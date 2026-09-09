from django.urls import path

from . import views


urlpatterns = [
    path("", views.property_list, name="property_list"),
    path("create/", views.property_create, name="property_create"),
    path(
        "<int:property_id>/",
        views.property_detail,
        name="property_detail",
    ),
    path(
        "<int:property_id>/edit/",
        views.property_update,
        name="property_update",
    ),
    path(
        "<int:property_id>/delete/",
        views.property_delete,
        name="property_delete",
    ),
]