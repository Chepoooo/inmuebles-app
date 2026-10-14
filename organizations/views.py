import cloudinary
import cloudinary.uploader

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from accounts.utils import (
    admin_required,
    get_current_membership,
    get_current_organization,
)

from .forms import OrganizationSettingsForm


@login_required
def organization_settings(request):

    organization = get_current_organization(request)

    if not organization:
        return redirect(
            "organization_select"
        )

    membership = get_current_membership(request)

    if request.method == "POST":

        if membership.role != "admin":
            return HttpResponseForbidden(
                "No tienes permisos para modificar "
                "la organización."
            )

        form = OrganizationSettingsForm(
            request.POST,
            request.FILES,
            instance=organization,
        )

        if form.is_valid():

            organization = form.save(
                commit=False
            )

            logo = request.FILES.get(
                "logo"
            )

            if logo:

                result = cloudinary.uploader.upload(
                    logo,
                    folder="organizations/logos",
                )

                old_public_id = (
                    organization.logo_public_id
                )

                if old_public_id:

                    cloudinary.uploader.destroy(
                        old_public_id
                    )

                organization.logo_public_id = (
                    result["public_id"]
                )

                organization.logo_secure_url = (
                    result["secure_url"]
                )

            organization.save()

            return redirect(
                "organization_settings"
            )

    else:

        form = OrganizationSettingsForm(
            instance=organization
        )

    return render(
        request,
        "organizations/organization_settings.html",
        {
            "organization": organization,
            "membership": membership,
            "form": form,
        },
    )