from django.urls import path

from . import views


urlpatterns = [
    path("", views.repair_list, name="repair_list"),
    path("create/", views.repair_create, name="repair_create"),
    path("<int:repair_id>/", views.repair_detail, name="repair_detail"),
    path(
        "<int:repair_id>/edit/",
        views.repair_update,
        name="repair_update",
    ),
    path(
        "<int:repair_id>/delete/",
        views.repair_delete,
        name="repair_delete",
    ),
    path(
    "<int:repair_id>/update-status/",
    views.repair_user_update,
    name="repair_user_update",
    ),
]