from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from organizations.models import Membership

def home(request):
    # Si no ha iniciado sesión, enviar al login.
    if not request.user.is_authenticated:
        return redirect("login")

    # Revisar si ya tiene una organización seleccionada
    # y si todavía tiene acceso a ella.
    organization_id = request.session.get("organization_id")

    if organization_id and Membership.objects.filter(
        user=request.user,
        organization_id=organization_id,
    ).exists():
        return redirect("property_list")

    # Sin organización seleccionada, dejar que la vista
    # existente gestione uno, varios o ningún membership.
    return redirect("organization_select")


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

