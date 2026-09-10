from django.contrib import admin

from .models import (
    Inventory,
    InventoryItem,
    InventoryItemPhoto,
    InventorySection,
)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "inventory_type",
        "created_at",
    )
    list_filter = ("inventory_type",)
    search_fields = (
        "property__name",
        "property__property_number",
    )


@admin.register(InventorySection)
class InventorySectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "inventory",
        "order",
    )
    list_filter = ("inventory",)
    search_fields = ("name",)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "section",
        "order",
    )
    list_filter = ("section",)
    search_fields = ("name",)
    
@admin.register(InventoryItemPhoto)
class InventoryItemPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "public_id",
        "created_at",
    )
    search_fields = (
        "item__name",
        "public_id",
    )