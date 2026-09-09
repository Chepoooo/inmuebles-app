from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.utils import get_current_organization
from properties.models import Property

from .forms import InventoryForm, InventoryItemForm
from .models import Inventory, InventoryItem, InventorySection


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
                    InventoryItem.objects.create(
                        section=section,
                        name=item_name,
                        order=item_order,
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

    inventory = get_object_or_404(
        Inventory.objects.select_related("property"),
        id=inventory_id,
        property__organization=organization,
    )

    sections = inventory.sections.prefetch_related("items")

    if request.method == "POST":
        for section in sections:
            for item in section.items.all():
                description = request.POST.get(
                    f"description_{item.id}",
                    "",
                )

                item.description = description
                item.save(
                    update_fields=["description"]
                )

        return redirect(
            "inventory_detail",
            inventory_id=inventory.id,
        )

    return render(
        request,
        "inventory/inventory_detail.html",
        {
            "inventory": inventory,
            "sections": sections,
        },
    )
    
@login_required
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