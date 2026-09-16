
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

    STATUS_CHOICES = [
        ("good", "Buen estado"),
        ("regular", "Regular"),
        ("bad", "Mal estado"),
    ]

    section = models.ForeignKey(
        InventorySection,
        on_delete=models.CASCADE,
        related_name="items",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Nombre",
    )

    item_type = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Tipo o material",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        verbose_name="Estado",
    )

    type_options = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Opciones de tipo o material",
    )

    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Datos adicionales",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Característica de inventario"
        verbose_name_plural = "Características de inventario"

    def __str__(self):
        return self.name
    
class InventoryItemPhoto(models.Model):
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    public_id = models.CharField(max_length=255)
    secure_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.item.name}"
    
class InventorySignature(models.Model):
    inventory = models.OneToOneField(
        Inventory,
        on_delete=models.CASCADE,
        related_name="signature",
    )
    name = models.CharField(max_length=150)
    public_id = models.CharField(max_length=255)
    secure_url = models.URLField(max_length=500)
    signed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signature for {self.inventory}"