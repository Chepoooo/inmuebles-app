
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.utils import admin_required
from accounts.utils import get_current_organization

from .forms import PropertyForm
from .models import Property


@login_required
def property_list(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    properties = Property.objects.filter(
        organization=organization
    )

    return render(
        request,
        "properties/property_list.html",
        {"properties": properties},
    )


@login_required
def property_detail(request, property_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    property = get_object_or_404(
        Property,
        id=property_id,
        organization=organization,
    )

    return render(
        request,
        "properties/property_detail.html",
        {"property": property},
    )


@login_required
@admin_required
def property_create(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    if request.method == "POST":
        form = PropertyForm(request.POST)

        if form.is_valid():
            property = form.save(commit=False)
            property.organization = organization
            property.save()

            return redirect(
                "property_detail",
                property_id=property.id,
            )
    else:
        form = PropertyForm()

    return render(
        request,
        "properties/property_form.html",
        {
            "form": form,
            "title": "Crear propiedad",
        },
    )


@login_required
@admin_required
def property_update(request, property_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    property = get_object_or_404(
        Property,
        id=property_id,
        organization=organization,
    )

    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property)

        if form.is_valid():
            form.save()

            return redirect(
                "property_detail",
                property_id=property.id,
            )
    else:
        form = PropertyForm(instance=property)

    return render(
        request,
        "properties/property_form.html",
        {
            "form": form,
            "title": "Editar propiedad",
        },
    )


@login_required
@admin_required
def property_delete(request, property_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    property = get_object_or_404(
        Property,
        id=property_id,
        organization=organization,
    )

    if request.method == "POST":
        property.delete()
        return redirect("property_list")

    return render(
        request,
        "properties/property_confirm_delete.html",
        {"property": property},
    )