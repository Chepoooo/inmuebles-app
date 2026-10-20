from organizations.models import Membership


def current_membership(request):
    organization_id = request.session.get("organization_id")

    if not request.user.is_authenticated or not organization_id:
        return {"current_membership": None}

    return {
        "current_membership": Membership.objects.filter(
            user=request.user,
            organization_id=organization_id,
        ).first(),
    }
