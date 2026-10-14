from django.urls import path

from . import views


urlpatterns = [
    path(
        "settings/",
        views.organization_settings,
        name="organization_settings",
    ),
]