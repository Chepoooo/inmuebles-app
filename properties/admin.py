from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "property_number",
        "tenant_name",
        "organization",
        "created_at",
    )
    list_filter = ("organization",)
    search_fields = (
        "name",
        "property_number",
        "tenant_name",
        "address",
    )