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
    path(
    "item/<int:item_id>/photos/add/",
    views.inventory_item_photo_create,
    name="inventory_item_photo_create",
    ),
    
    path(
    "photo/<int:photo_id>/delete/",
    views.inventory_item_photo_delete,
    name="inventory_item_photo_delete",  
    ),
    path(
    "<int:inventory_id>/signature/",
    views.inventory_signature_create,
    name="inventory_signature_create",
    ),
    path(
    "",
    views.inventory_dashboard,
    name="inventory_dashboard",
    ),
    path(
    "inventory/<int:inventory_id>/section/create/",
    views.inventory_section_create,
    name="inventory_section_create",
    ),
    path(
    "inventory/<int:inventory_id>/add-auxiliary-bedroom/",
    views.inventory_add_auxiliary_bedroom,
    name="inventory_add_auxiliary_bedroom",
    ),

    path(
        "inventory/<int:inventory_id>/add-auxiliary-bathroom/",
        views.inventory_add_auxiliary_bathroom,
        name="inventory_add_auxiliary_bathroom",
    ),
]