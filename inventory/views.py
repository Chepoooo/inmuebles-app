from django.contrib.auth.decorators import login_required
from inventory.utils import save_inventory_from_post
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponseForbidden
from django.utils.text import slugify
import cloudinary

import cloudinary.uploader

from django.db.models import Q

from accounts.utils import (
    admin_required,
    get_current_membership,
    get_current_organization,
)

from properties.models import Property

from .defaults import (
    DEFAULT_DECLARATION,
    INVENTORY_SECTION_DEFINITIONS,
    KEYS_SECTION_NAME,
)

from .forms import (
    InventoryForm,
    InventoryItemForm,
    InventoryNoteForm,
    InventorySectionForm,
)

from .models import (
    Inventory,
    InventoryItem,
    InventoryItemPhoto,
    InventoryNote,
    InventorySection,
    InventorySignature,
    InventorySignaturePhoto,
)

from .pdf import build_inventory_pdf


@login_required
def inventory_list(request, property_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    property = get_object_or_404(
        Property,
        id=property_id,
        organization=organization,
    )

    inventories = Inventory.objects.filter(
        property=property
    )

    return render(
        request,
        "inventory/inventory_list.html",
        {
            "property": property,
            "inventories": inventories,
        },
    )


@login_required
@admin_required
def inventory_create(request, property_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    property = get_object_or_404(
        Property,
        id=property_id,
        organization=organization,
    )

    if request.method == "POST":
        form = InventoryForm(request.POST)

        if form.is_valid():

            inventory = form.save(commit=False)
            inventory.property = property
            inventory.save()

            for section_order, (section_name, items) in enumerate(
                INVENTORY_SECTION_DEFINITIONS.items()
            ):

                section = InventorySection.objects.create(
                    inventory=inventory,
                    name=section_name,
                    order=section_order,
                )

                for item_order, item_definition in enumerate(items):

                    item_name = item_definition["name"]

                    type_options = item_definition.get(
                        "type_options",
                        [],
                    )

                    extra_fields = item_definition.get(
                        "extra_fields",
                        {},
                    )

                    is_description = item_definition.get(
                        "is_description",
                        False,
                    )

                    extra_data = {}

                    for field_name in extra_fields:
                        extra_data[field_name] = ""

                    InventoryItem.objects.create(
                        section=section,
                        name=item_name,
                        order=item_order,
                        type_options=type_options,
                        extra_data=extra_data,
                        is_description=is_description,
                    )

            return redirect(
                "inventory_detail",
                inventory_id=inventory.id,
            )

    else:
        form = InventoryForm()

    return render(
        request,
        "inventory/inventory_form.html",
        {
            "form": form,
            "property": property,
            "title": "Crear inventario",
        },
    )


@login_required
def inventory_detail(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    membership = get_current_membership(request)

    if not membership or membership.role not in ("admin", "viewer"):
        return HttpResponseForbidden(
            "No tienes permisos para realizar esta acción."
        )

    read_only = membership.role != "admin"

    inventory = get_object_or_404(
        Inventory.objects.select_related(
            "property",
            "signature",
        ).prefetch_related(
            "signature__photos",
        ),
        id=inventory_id,
        property__organization=organization,
    )

    sections = inventory.sections.prefetch_related(
        "items__photos"
    )

    if request.method == "POST":

        if read_only:
            return HttpResponseForbidden(
                "No tienes permisos para realizar esta acción."
            )

        save_inventory_from_post(
            request,
            inventory,
        )

        if request.POST.get("action") == "sign":
            return redirect(
                "inventory_signature_create",
                inventory_id=inventory.id,
            )

        return redirect(
            "inventory_detail",
            inventory_id=inventory.id,
        )

    # Preparar los campos adicionales para mostrar
    # correctamente en el template.
    for section in sections:

        for item in section.items.all():

            item.extra_fields = {}

            # Las secciones dinámicas utilizan la definición
            # de su sección original.
            base_section_name = section.name

            if section.name.startswith("Alcoba auxiliar "):
                base_section_name = "Alcoba auxiliar"

            elif section.name.startswith("Baño auxiliar "):
                base_section_name = "Baño auxiliar"

            for section_name, definitions in INVENTORY_SECTION_DEFINITIONS.items():

                if base_section_name == section_name:

                    for definition in definitions:

                        if definition["name"] == item.name:

                            item.extra_fields = definition.get(
                                "extra_fields",
                                {},
                            )

                            break

    return render(
        request,
        "inventory/inventory_detail.html",
        {
            "inventory": inventory,
            "sections": sections,
            "status_choices": InventoryItem.STATUS_CHOICES,
            "membership": membership,
            "read_only": read_only,
            "has_keys_section": inventory.sections.filter(
                name=KEYS_SECTION_NAME,
            ).exists(),
        },
    )
    
@login_required
@admin_required
def inventory_item_create(request, section_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    section = get_object_or_404(
        InventorySection.objects.select_related(
            "inventory__property"
        ),
        id=section_id,
        inventory__property__organization=organization,
    )

    if request.method == "POST":
        form = InventoryItemForm(request.POST)

        if form.is_valid():

            item = form.save(commit=False)

            item.section = section
            item.order = (
                section.items.order_by("-order")
                .values_list("order", flat=True)
                .first()
            )

            if item.order is None:
                item.order = 0
            else:
                item.order += 1

            item.type_options = []
            item.extra_data = {}
            item.is_description = False

            item.save()

            return redirect(
                "inventory_detail",
                inventory_id=section.inventory.id,
            )

    else:
        form = InventoryItemForm()

    return render(
        request,
        "inventory/inventory_item_form.html",
        {
            "form": form,
            "section": section,
            "inventory": section.inventory,
            "title": "Agregar característica",
        },
    )
    
@login_required
@admin_required
def inventory_item_update(request, item_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    item = get_object_or_404(
        InventoryItem.objects.select_related(
            "section__inventory__property"
        ),
        id=item_id,
        section__inventory__property__organization=organization,
    )

    if request.method == "POST":
        form = InventoryItemForm(
            request.POST,
            instance=item,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "inventory_detail",
                inventory_id=item.section.inventory_id,
            )

    else:
        form = InventoryItemForm(
            instance=item
        )

    return render(
        request,
        "inventory/inventory_item_form.html",
        {
            "form": form,
            "section": item.section,
            "inventory": item.section.inventory,
            "title": "Editar característica",
        },
    )
    
@login_required
@admin_required
def inventory_item_delete(request, item_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    item = get_object_or_404(
        InventoryItem.objects.select_related(
            "section__inventory__property"
        ),
        id=item_id,
        section__inventory__property__organization=organization,
    )

    inventory = item.section.inventory
    inventory_id = inventory.id

    if request.method == "POST":

        # Primer paso: guardar el inventario antes de mostrar
        # la confirmación de eliminación.
        if request.POST.get("prepare_delete") == "1":
            save_inventory_from_post(request, inventory)

            return render(
                request,
                "inventory/inventory_item_confirm_delete.html",
                {
                    "item": item,
                },
            )

        # Segundo paso: eliminar solo cuando se confirma.
        if request.POST.get("confirm_delete") == "1":
            item.delete()

            return redirect(
                "inventory_detail",
                inventory_id=inventory_id,
            )

    return render(
        request,
        "inventory/inventory_item_confirm_delete.html",
        {
            "item": item,
        },
    )
    
@login_required
@admin_required
def inventory_item_photo_create(request, item_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    item = get_object_or_404(
        InventoryItem.objects.select_related(
            "section__inventory__property"
        ),
        id=item_id,
        section__inventory__property__organization=organization,
    )

    inventory = item.section.inventory

    if request.method == "POST":

        # Guardar primero los cambios del inventario.
        if request.POST.get("prepare_photo") == "1":
            save_inventory_from_post(
                request,
                inventory,
            )

            return render(
                request,
                "inventory/inventory_item_photo_form.html",
                {
                    "item": item,
                },
            )

        # Subir la foto después de que el usuario la seleccione.
        photo = request.FILES.get("photo")

        if photo:
            result = cloudinary.uploader.upload(
                photo,
                folder="inventory",
            )

            InventoryItemPhoto.objects.create(
                item=item,
                public_id=result["public_id"],
                secure_url=result["secure_url"],
            )

            return redirect(
                "inventory_detail",
                inventory_id=inventory.id,
            )

    return render(
        request,
        "inventory/inventory_item_photo_form.html",
        {
            "item": item,
        },
    )
    
@login_required
@admin_required
def inventory_item_photo_delete(request, photo_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    photo = get_object_or_404(
        InventoryItemPhoto.objects.select_related(
            "item__section__inventory__property"
        ),
        id=photo_id,
        item__section__inventory__property__organization=organization,
    )

    inventory = photo.item.section.inventory
    inventory_id = inventory.id

    if request.method == "POST":

        # Guardar primero los cambios del inventario.
        if request.POST.get("prepare_delete_photo") == "1":
            save_inventory_from_post(
                request,
                inventory,
            )

            return render(
                request,
                "inventory/inventory_item_photo_confirm_delete.html",
                {
                    "photo": photo,
                },
            )

        # Eliminar la foto únicamente tras confirmar.
        if request.POST.get("confirm_delete_photo") == "1":
            cloudinary.uploader.destroy(photo.public_id)
            photo.delete()

            return redirect(
                "inventory_detail",
                inventory_id=inventory_id,
            )

    return render(
        request,
        "inventory/inventory_item_photo_confirm_delete.html",
        {
            "photo": photo,
        },
    )
    
@login_required
@admin_required
def inventory_signature_create(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory.objects.select_related("property"),
        id=inventory_id,
        property__organization=organization,
    )

    if hasattr(inventory, "signature"):
        return redirect(
            "inventory_detail",
            inventory_id=inventory.id,
        )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            "",
        ).strip()

        document_type = request.POST.get(
            "document_type",
            "",
        ).strip()

        document_number = request.POST.get(
            "document_number",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip()

        selected_note_ids = request.POST.getlist(
            "notes"
        )

        new_note_title = request.POST.get(
            "new_note_title",
            "",
        ).strip()

        new_note_content = request.POST.get(
            "new_note_content",
            "",
        ).strip()

        signature_data = request.POST.get(
            "signature",
            "",
        ).strip()

        photos = request.FILES.getlist(
            "photos"
        )

        # ----------------------------------------------------
        # Validar cantidad de fotos
        # ----------------------------------------------------

        if len(photos) > 5:

            return render(
                request,
                "inventory/inventory_signature_form.html",
                {
                    "inventory": inventory,
                    "notes": organization.notes.all(),
                    "default_declaration": (
                        DEFAULT_DECLARATION
                    ),
                    "document_type_choices": (
                        Property.DocumentType.choices
                    ),
                    "photo_error": (
                        "Puedes subir un máximo "
                        "de 5 fotos como evidencia."
                    ),
                },
            )

        # ----------------------------------------------------
        # Crear firma
        # ----------------------------------------------------

        if name and signature_data:

            # --------------------------------------------
            # Construir el snapshot de notas y
            # declaraciones que el cliente aceptó.
            # --------------------------------------------

            notes_snapshot = [
                {
                    "title": "Declaración",
                    "content": DEFAULT_DECLARATION,
                }
            ]

            if selected_note_ids:

                selected_notes = (
                    InventoryNote.objects.filter(
                        organization=organization,
                        id__in=selected_note_ids,
                    )
                )

                for note in selected_notes:

                    notes_snapshot.append(
                        {
                            "title": note.title,
                            "content": note.content,
                        }
                    )

            if new_note_content:

                note_title = (
                    new_note_title or "Nota personalizada"
                )

                new_note = InventoryNote.objects.create(
                    organization=organization,
                    title=note_title,
                    content=new_note_content,
                )

                notes_snapshot.append(
                    {
                        "title": new_note.title,
                        "content": new_note.content,
                    }
                )

            result = cloudinary.uploader.upload(
                signature_data,
                folder="inventory/signatures",
            )

            signature = InventorySignature.objects.create(
                inventory=inventory,
                name=name,
                document_type=document_type,
                document_number=document_number,
                email=email,
                notes_snapshot=notes_snapshot,
                public_id=result["public_id"],
                secure_url=result["secure_url"],
            )

            # ------------------------------------------------
            # Subir evidencias
            # ------------------------------------------------

            for photo in photos:

                photo_result = (
                    cloudinary.uploader.upload(
                        photo,
                        folder="inventory/signatures/evidence",
                    )
                )

                InventorySignaturePhoto.objects.create(
                    signature=signature,
                    public_id=photo_result[
                        "public_id"
                    ],
                    secure_url=photo_result[
                        "secure_url"
                    ],
                )

            return redirect(
                "inventory_detail",
                inventory_id=inventory.id,
            )

    return render(
        request,
        "inventory/inventory_signature_form.html",
        {
            "inventory": inventory,
            "notes": organization.notes.all(),
            "default_declaration": DEFAULT_DECLARATION,
            "document_type_choices": (
                Property.DocumentType.choices
            ),
        },
    )
    
@login_required
def inventory_dashboard(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventories = (
        Inventory.objects
        .filter(property__organization=organization)
        .select_related(
            "property",
            "signature",
        )
    )

    search = request.GET.get("search", "").strip()

    if search:
        inventories = inventories.filter(
            Q(property__name__icontains=search)
            | Q(property__property_number__icontains=search)
            | Q(signature__name__icontains=search)
        )

    paginator = Paginator(inventories, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventory/inventory_dashboard.html",
        {
            "inventories": page_obj,
            "page_obj": page_obj,
            "search": search,
            "membership": get_current_membership(request),
        },
    )
    
    
@login_required
def inventory_pdf(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory.objects.select_related(
            "property__organization",
            "signature",
        ).prefetch_related(
            "sections__items__photos",
            "signature__photos",
        ),
        id=inventory_id,
        property__organization=organization,
    )

    pdf_buffer = build_inventory_pdf(
        inventory,
        INVENTORY_SECTION_DEFINITIONS,
    )

    property_name = slugify(
        inventory.property.name
    )

    if not property_name:
        property_name = (
            f"inventory-{inventory.id}"
        )

    filename = (
        f"inventario-"
        f"{property_name}-"
        f"{inventory.inventory_type}.pdf"
    )

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename=filename,
        content_type="application/pdf",
    )
    
    
    
    
    
@login_required
@admin_required
def inventory_section_create(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
        property__organization=organization,
    )

    if request.method == "POST":
        form = InventorySectionForm(request.POST)

        if form.is_valid():

            section = form.save(commit=False)
            section.inventory = inventory

            last_section = inventory.sections.order_by("-order").first()

            if last_section:
                section.order = last_section.order + 1
            else:
                section.order = 0

            section.save()

            return redirect(
                "inventory_detail",
                inventory_id=inventory.id,
            )

    else:
        form = InventorySectionForm()

    return render(
        request,
        "inventory/inventory_section_form.html",
        {
            "form": form,
            "inventory": inventory,
        },
    )
    
@login_required
@admin_required
def inventory_add_auxiliary_bedroom(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
        property__organization=organization,
    )

    existing_sections = inventory.sections.filter(
        name__startswith="Alcoba auxiliar"
    )

    numbers = []

    for section in existing_sections:

        if section.name == "Alcoba auxiliar":
            numbers.append(1)

        else:
            suffix = section.name.replace(
                "Alcoba auxiliar ",
                "",
                1,
            )

            if suffix.isdigit():
                numbers.append(int(suffix))

    next_number = max(numbers, default=1) + 1

    section_name = f"Alcoba auxiliar {next_number}"

    last_section = inventory.sections.order_by("-order").first()

    if last_section:
        section_order = last_section.order + 1
    else:
        section_order = 0

    section = InventorySection.objects.create(
        inventory=inventory,
        name=section_name,
        order=section_order,
    )

    definitions = INVENTORY_SECTION_DEFINITIONS[
        "Alcoba auxiliar"
    ]

    for item_order, item_definition in enumerate(definitions):

        extra_fields = item_definition.get(
            "extra_fields",
            {},
        )

        extra_data = {}

        for field_name in extra_fields:
            extra_data[field_name] = ""

        InventoryItem.objects.create(
            section=section,
            name=item_definition["name"],
            order=item_order,
            type_options=item_definition.get(
                "type_options",
                [],
            ),
            extra_data=extra_data,
            is_description=item_definition.get(
                "is_description",
                False,
            ),
        )

    return redirect(
        "inventory_detail",
        inventory_id=inventory.id,
    )


@login_required
@admin_required
def inventory_add_auxiliary_bathroom(request, inventory_id):



    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
        property__organization=organization,
    )

    existing_sections = inventory.sections.filter(
        name__startswith="Baño auxiliar"
    )

    numbers = []

    for section in existing_sections:

        if section.name == "Baño auxiliar":
            numbers.append(1)

        else:
            suffix = section.name.replace(
                "Baño auxiliar ",
                "",
                1,
            )

            if suffix.isdigit():
                numbers.append(int(suffix))

    next_number = max(numbers, default=1) + 1

    section_name = f"Baño auxiliar {next_number}"

    last_section = inventory.sections.order_by("-order").first()

    if last_section:
        section_order = last_section.order + 1
    else:
        section_order = 0

    section = InventorySection.objects.create(
        inventory=inventory,
        name=section_name,
        order=section_order,
    )

    definitions = INVENTORY_SECTION_DEFINITIONS[
        "Baño auxiliar"
    ]

    for item_order, item_definition in enumerate(definitions):

        extra_fields = item_definition.get(
            "extra_fields",
            {},
        )

        extra_data = {}

        for field_name in extra_fields:
            extra_data[field_name] = ""

        InventoryItem.objects.create(
            section=section,
            name=item_definition["name"],
            order=item_order,
            type_options=item_definition.get(
                "type_options",
                [],
            ),
            extra_data=extra_data,
            is_description=item_definition.get(
                "is_description",
                False,
            ),
        )

    return redirect(
        "inventory_detail",
        inventory_id=inventory.id,
    )
    

@login_required
@admin_required
def inventory_add_keys(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
        property__organization=organization,
    )

    # No duplicar la sección si ya existe
    if inventory.sections.filter(
        name=KEYS_SECTION_NAME,
    ).exists():

        return redirect(
            "inventory_detail",
            inventory_id=inventory.id,
        )

    last_section = inventory.sections.order_by(
        "-order"
    ).first()

    if last_section:
        section_order = last_section.order + 1
    else:
        section_order = 0

    section = InventorySection.objects.create(
        inventory=inventory,
        name=KEYS_SECTION_NAME,
        order=section_order,
    )

    InventoryItem.objects.create(
        section=section,
        name="Cantidad de llaves",
        order=0,
        extra_data={"quantity": ""},
    )

    return redirect(
        "inventory_detail",
        inventory_id=inventory.id,
    )


@login_required
@admin_required
def inventory_section_delete(request, section_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    section = get_object_or_404(
        InventorySection.objects.select_related(
            "inventory__property"
        ),
        id=section_id,
        inventory__property__organization=organization,
    )

    inventory = section.inventory
    inventory_id = inventory.id

    if request.method == "POST":

        # Primer paso: guardar el inventario antes de mostrar
        # la confirmación de eliminación.
        if request.POST.get("prepare_delete") == "1":
            save_inventory_from_post(request, inventory)

            return render(
                request,
                "inventory/inventory_section_confirm_delete.html",
                {
                    "section": section,
                    "inventory": inventory,
                },
            )

        # Segundo paso: eliminar solo cuando se confirma.
        if request.POST.get("confirm_delete") == "1":
            section.delete()

            return redirect(
                "inventory_detail",
                inventory_id=inventory_id,
            )

    return render(
        request,
        "inventory/inventory_section_confirm_delete.html",
        {
            "section": section,
            "inventory": inventory,
        },
    )
    
@login_required
@admin_required
def inventory_delete(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
        property__organization=organization,
    )

    if request.method == "POST":
        inventory.delete()

        return redirect(
            "inventory_dashboard"
        )

    return render(
        request,
        "inventory/inventory_confirm_delete.html",
        {
            "inventory": inventory,
        },
    )


# ================================================================
# NOTAS Y DECLARACIONES
# ================================================================

@login_required
@admin_required
def inventory_notes(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    notes = organization.notes.all()

    return render(
        request,
        "inventory/inventory_notes.html",
        {
            "notes": notes,
            "organization": organization,
        },
    )


@login_required
@admin_required
def inventory_note_create(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    if request.method == "POST":

        form = InventoryNoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)
            note.organization = organization
            note.save()

            return redirect("inventory_notes")

    else:
        form = InventoryNoteForm()

    return render(
        request,
        "inventory/inventory_note_form.html",
        {
            "form": form,
            "title": "Nueva nota",
        },
    )


@login_required
@admin_required
def inventory_note_update(request, note_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    note = get_object_or_404(
        InventoryNote,
        id=note_id,
        organization=organization,
    )

    if request.method == "POST":

        form = InventoryNoteForm(
            request.POST,
            instance=note,
        )

        if form.is_valid():
            form.save()
            return redirect("inventory_notes")

    else:
        form = InventoryNoteForm(instance=note)

    return render(
        request,
        "inventory/inventory_note_form.html",
        {
            "form": form,
            "title": "Editar nota",
        },
    )


@login_required
@admin_required
def inventory_note_delete(request, note_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    note = get_object_or_404(
        InventoryNote,
        id=note_id,
        organization=organization,
    )

    if request.method == "POST":
        note.delete()
        return redirect("inventory_notes")

    return render(
        request,
        "inventory/inventory_note_confirm_delete.html",
        {
            "note": note,
        },
    )