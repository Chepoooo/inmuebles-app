from django.shortcuts import get_object_or_404

from organizations.models import Membership


def get_current_membership(request):
    organization_id = request.session.get("organization_id")

    if not organization_id:
        return None

    return get_object_or_404(
        Membership.objects.select_related("organization"),
        user=request.user,
        organization_id=organization_id,
    )


def get_current_organization(request):
    membership = get_current_membership(request)

    if not membership:
        return None

    return membership.organization