from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from organizations.models import Membership


@login_required
def organization_select(request):
    memberships = Membership.objects.filter(
        user=request.user
    ).select_related("organization")

    if not memberships.exists():
        return render(
            request,
            "accounts/no_organization.html",
        )

    if memberships.count() == 1:
        request.session["organization_id"] = memberships.first().organization_id
        return redirect("property_list")

    return render(
        request,
        "accounts/organization_select.html",
        {"memberships": memberships},
    )


@login_required
def organization_set(request, membership_id):
    membership = get_object_or_404(
        Membership,
        id=membership_id,
        user=request.user,
    )

    request.session["organization_id"] = membership.organization_id

    return redirect("property_list")

