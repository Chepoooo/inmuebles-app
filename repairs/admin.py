from django.contrib import admin

from .models import Repair, RepairPhoto


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = (
        "repair_type",
        "property",
        "assigned_worker",
        "status",
        "report_date",
        "quote",
    )
    list_filter = (
        "status",
        "report_date",
    )
    search_fields = (
        "repair_type",
        "property__name",
        "property__property_number",
        "assigned_worker",
    )
    
@admin.register(RepairPhoto)
class RepairPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "repair",
        "public_id",
        "created_at",
    )
    search_fields = (
        "repair__repair_type",
        "repair__property__name",
        "public_id",
    )