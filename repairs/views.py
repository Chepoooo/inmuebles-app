from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from .forms import RepairForm, RepairUserForm
from accounts.utils import (
    admin_required,
    get_current_organization,
    user_is_repair_user,
)
from accounts.utils import admin_required, get_current_organization
from .forms import RepairForm
from .models import Repair


@login_required
def repair_list(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    repairs = (
        Repair.objects
        .filter(organization=organization)
        .select_related("property")
    )

    return render(
        request,
        "repairs/repair_list.html",
        {"repairs": repairs},
    )


@login_required
def repair_detail(request, repair_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    repair = get_object_or_404(
        Repair.objects.select_related("property"),
        id=repair_id,
        organization=organization,
    )

    return render(
        request,
        "repairs/repair_detail.html",
        {"repair": repair},
    )


@login_required
@admin_required
def repair_create(request):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    if request.method == "POST":
        form = RepairForm(request.POST)

        form.fields["property"].queryset = organization.properties.all()

        if form.is_valid():
            repair = form.save(commit=False)
            repair.organization = organization
            repair.save()

            return redirect(
                "repair_detail",
                repair_id=repair.id,
            )
    else:
        form = RepairForm()
        form.fields["property"].queryset = organization.properties.all()

    return render(
        request,
        "repairs/repair_form.html",
        {
            "form": form,
            "title": "Crear reparación",
        },
    )


@login_required
@admin_required
def repair_update(request, repair_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    repair = get_object_or_404(
        Repair,
        id=repair_id,
        organization=organization,
    )

    if request.method == "POST":
        form = RepairForm(
            request.POST,
            instance=repair,
        )

        form.fields["property"].queryset = organization.properties.all()

        if form.is_valid():
            form.save()

            return redirect(
                "repair_detail",
                repair_id=repair.id,
            )
    else:
        form = RepairForm(instance=repair)
        form.fields["property"].queryset = organization.properties.all()

    return render(
        request,
        "repairs/repair_form.html",
        {
            "form": form,
            "title": "Editar reparación",
        },
    )


@login_required
@admin_required
def repair_delete(request, repair_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    repair = get_object_or_404(
        Repair,
        id=repair_id,
        organization=organization,
    )

    if request.method == "POST":
        repair.delete()
        return redirect("repair_list")

    return render(
        request,
        "repairs/repair_confirm_delete.html",
        {"repair": repair},
    )
    
@login_required
def repair_user_update(request, repair_id):
    organization = get_current_organization(request)

    if not organization:
        return redirect("organization_select")

    if not user_is_repair_user(request):
        return HttpResponseForbidden(
            "No tienes permisos para realizar esta acción."
        )

    repair = get_object_or_404(
        Repair,
        id=repair_id,
        organization=organization,
    )

    if request.method == "POST":
        form = RepairUserForm(
            request.POST,
            instance=repair,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "repair_detail",
                repair_id=repair.id,
            )
    else:
        form = RepairUserForm(instance=repair)

    return render(
        request,
        "repairs/repair_user_form.html",
        {
            "form": form,
            "repair": repair,
        },
    )