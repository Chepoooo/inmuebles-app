from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
    "organizations/",
    views.organization_select,
    name="organization_select",
    ),
    path(
        "organizations/<int:membership_id>/select/",
        views.organization_set,
        name="organization_set",
   ),
   
]