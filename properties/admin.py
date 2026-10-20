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
        "document_type",
        "document_number",
        "organization",
        "created_at",
    )
    list_filter = ("organization", "document_type")
    search_fields = (
        "name",
        "property_number",
        "tenant_name",
        "document_number",
        "address",
    )