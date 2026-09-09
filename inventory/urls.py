from django.urls import path

from . import views


urlpatterns = [
    path(
        "property/<int:property_id>/",
        views.inventory_list,
        name="inventory_list",
    ),
    path(
        "property/<int:property_id>/create/",
        views.inventory_create,
        name="inventory_create",
    ),
    path(
        "<int:inventory_id>/",
        views.inventory_detail,
        name="inventory_detail",
    ),
    path(
        "section/<int:section_id>/add-item/",
        views.inventory_item_create,
        name="inventory_item_create",
    ),
    path(
    "item/<int:item_id>/edit/",
    views.inventory_item_update,
    name="inventory_item_update",
    ),
    path(
    "item/<int:item_id>/delete/",
    views.inventory_item_delete,
    name="inventory_item_delete",
    ),
]