from django.shortcuts import get_object_or_404
from functools import wraps

from django.http import HttpResponseForbidden

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

def user_has_role(request, role):
    membership = get_current_membership(request)

    if not membership:
        return False

    return membership.role == role

def user_is_admin(request):
    return user_has_role(
        request,
        Membership.Role.ADMIN,
    )


def user_is_viewer(request):
    return user_has_role(
        request,
        Membership.Role.VIEWER,
    )


def user_is_repair_user(request):
    return user_has_role(
        request,
        Membership.Role.REPAIR_USER,
    )
    
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not user_is_admin(request):
            return HttpResponseForbidden(
                "No tienes permisos para realizar esta acción."
            )

        return view_func(request, *args, **kwargs)

    return wrapper