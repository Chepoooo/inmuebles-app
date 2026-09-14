
from django.db import models

from organizations.models import Organization


class Property(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="properties",
    )
    
    photo_public_id = models.CharField(
    max_length=255,
    blank=True,
    )

    photo_url = models.URLField(
        max_length=500,
        blank=True,
    )
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    property_number = models.CharField(max_length=100)
    tenant_name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.property_number}"