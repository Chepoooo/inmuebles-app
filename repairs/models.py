from django.db import models

from organizations.models import Organization
from properties.models import Property
from inventory.models import InventoryItem


class Repair(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        IN_PROGRESS = "in_progress", "En progreso"
        COMPLETED = "completed", "Completada"
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="repairs",
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="repairs",
    )

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repairs",
    )

    repair_type = models.CharField(max_length=150)

    report_date = models.DateField()

    assigned_worker = models.CharField(
        max_length=150,
        blank=True,
    )

    quote = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.repair_type} - {self.property}"


class RepairPhoto(models.Model):
    repair = models.ForeignKey(
        Repair,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    public_id = models.CharField(max_length=255)

    secure_url = models.URLField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.repair}"