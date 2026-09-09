
# Create your models here.
from django.db import models

from properties.models import Property


class Inventory(models.Model):
    class InventoryType(models.TextChoices):
        INITIAL = "initial", "Initial"
        FINAL = "final", "Final"

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="inventories",
    )
    inventory_type = models.CharField(
        max_length=10,
        choices=InventoryType.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.name} - {self.get_inventory_type_display()}"


class InventorySection(models.Model):
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    name = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    section = models.ForeignKey(
        InventorySection,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name