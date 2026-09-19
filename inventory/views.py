from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render

import cloudinary

import cloudinary.uploader

from django.db.models import Q

from accounts.utils import (
    admin_required,
    get_current_membership,
    get_current_organization,
)

from properties.models import Property

from .defaults import INVENTORY_SECTION_DEFINITIONS

from .forms import (
    InventoryForm,
    InventoryItemForm,
    InventorySectionForm,
)

from .models import (
    Inventory,
    InventoryItem,
    InventoryItemPhoto,
    InventorySection,
    InventorySignature,
)


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
@admin_required
def inventory_detail(request, inventory_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    membership = get_current_membership(request)

    inventory = get_object_or_404(
        Inventory.objects.select_related("property"),
        id=inventory_id,
        property__organization=organization,
    )

    sections = inventory.sections.prefetch_related(
        "items__photos"
    )

    if request.method == "POST":

        has_errors = False

        for section in sections:

            for item in section.items.all():

                # Descripción adicional
                # No necesita estado, tipo ni material.
                if item.is_description:

                    item.description = request.POST.get(
                        f"description_{item.id}",
                        "",
                    ).strip()

                    item.save(
                        update_fields=[
                            "description",
                        ]
                    )

                    continue

                status = request.POST.get(
                    f"status_{item.id}",
                    "",
                ).strip()

                item_type = request.POST.get(
                    f"item_type_{item.id}",
                    "",
                ).strip()

                description = request.POST.get(
                    f"description_{item.id}",
                    "",
                ).strip()

                if not status:
                    has_errors = True
                    continue

                # Las secciones dinámicas utilizan la definición
                # de su sección original
                base_section_name = section.name

                if section.name.startswith("Alcoba auxiliar "):
                    base_section_name = "Alcoba auxiliar"

                elif section.name.startswith("Baño auxiliar "):
                    base_section_name = "Baño auxiliar"

                extra_fields = {}

                for section_name, definitions in INVENTORY_SECTION_DEFINITIONS.items():

                    if base_section_name == section_name:

                        for definition in definitions:

                            if definition["name"] == item.name:

                                extra_fields = definition.get(
                                    "extra_fields",
                                    {},
                                )

                                break

                extra_data = {}

                for field_name in extra_fields:

                    value = request.POST.get(
                        f"extra_{field_name}_{item.id}",
                        "",
                    ).strip()

                    extra_data[field_name] = value

                item.status = status
                item.item_type = item_type
                item.description = description
                item.extra_data = extra_data

                item.save(
                    update_fields=[
                        "status",
                        "item_type",
                        "description",
                        "extra_data",
                    ]
                )

        if not has_errors:
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

    inventory_id = item.section.inventory_id

    if request.method == "POST":
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

    if request.method == "POST":
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
                inventory_id=item.section.inventory_id,
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

    inventory_id = photo.item.section.inventory_id

    if request.method == "POST":
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
        name = request.POST.get("name", "").strip()
        signature_data = request.POST.get("signature", "").strip()

        if name and signature_data:
            result = cloudinary.uploader.upload(
                signature_data,
                folder="inventory/signatures",
            )

            InventorySignature.objects.create(
                inventory=inventory,
                name=name,
                public_id=result["public_id"],
                secure_url=result["secure_url"],
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
        },
    )
    
@login_required
def inventory_dashboard(request):
    organization = get_current_organization(request)

    inventories = (
        Inventory.objects
        .filter(property__organization=organization)
        .select_related("property")
    )

    search = request.GET.get("search", "").strip()

    if search:
        inventories = inventories.filter(
            Q(property__name__icontains=search)
            | Q(property__property_number__icontains=search)
        )

    return render(
        request,
        "inventory/inventory_dashboard.html",
        {
            "inventories": inventories,
            "search": search,
        },
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

    inventory_id = section.inventory.id

    if request.method == "POST":
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
            "inventory": section.inventory,
        },
    )