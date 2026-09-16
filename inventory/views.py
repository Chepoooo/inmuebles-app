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

from .defaults import (
    INVENTORY_ITEM_EXTRA_FIELDS,
    INVENTORY_ITEM_TYPE_OPTIONS,
)

from .forms import InventoryForm, InventoryItemForm

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

            sections_data = {
                "Entrada": [
                    "Puerta",
                    "Pisos",
                    "Paredes",
                    "Lámpara",
                    "Descripción adicional",
                ],
                "Sala - comedor": [
                    "Pisos",
                    "Paredes",
                    "Lámparas",
                    "Tomacorrientes",
                    "Interruptores",
                    "Puertas",
                    "Ventanas",
                    "Descripción adicional",
                ],
                "Balcón": [
                    "Puertas",
                    "Pisos",
                    "Paredes",
                    "Lámparas",
                    "Tomacorrientes",
                    "Interruptores",
                    "Baranda",
                    "Descripción adicional",
                ],
                "Cocina": [
                    "Puertas",
                    "Pisos",
                    "Paredes",
                    "Lámparas",
                    "Tomacorriente",
                    "Interruptores",
                    "Ventanas",
                    "Muebles flotante",
                    "Muebles inferiores",
                    "Mesón",
                    "Estufa",
                    "Horno",
                    "Campana",
                    "Descripción adicional",
                ],
                "Área de labores": [
                    "Puertas",
                    "Pisos",
                    "Paredes",
                    "Lámparas",
                    "Tomacorriente",
                    "Interruptores",
                    "Ventanas",
                    "Llaves de agua",
                    "Llaves de gas",
                    "Cifones",
                    "Lavadero",
                    "Caja de tacos",
                    "Descripción adicional",
                ],
                "Hall de alcobas": [
                    "Descripción adicional",
                ],
                "Alcoba principal": [
                    "Puertas",
                    "Pisos",
                    "Paredes",
                    "Lámparas",
                    "Tomacorriente",
                    "Interruptores",
                    "Ventanas",
                    "Clóset",
                    "Vestier",
                    "Descripción adicional",
                ],
            }

            for section_order, (section_name, items) in enumerate(
                sections_data.items()
            ):
                section = InventorySection.objects.create(
                    inventory=inventory,
                    name=section_name,
                    order=section_order,
                )

                for item_order, item_name in enumerate(items):

                    type_options = INVENTORY_ITEM_TYPE_OPTIONS.get(
                        item_name,
                        [],
                    )

        

                    InventoryItem.objects.create(
                        section=section,
                        name=item_name,
                        order=item_order,
                        type_options=type_options,
                        extra_data={},
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

                extra_fields = INVENTORY_ITEM_EXTRA_FIELDS.get(
                    item.name,
                    {},
                )

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

    for section in sections:

        for item in section.items.all():

            item.extra_fields = INVENTORY_ITEM_EXTRA_FIELDS.get(
                item.name,
                {},
            )

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
            item.order = section.items.count()
            item.save()

            return redirect(
                "inventory_detail",
                inventory_id=section.inventory_id,
            )
    else:
        form = InventoryItemForm()

    return render(
        request,
        "inventory/inventory_item_form.html",
        {
            "form": form,
            "section": section,
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
        form = InventoryItemForm(instance=item)

    return render(
        request,
        "inventory/inventory_item_form.html",
        {
            "form": form,
            "section": item.section,
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