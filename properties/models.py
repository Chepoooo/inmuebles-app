from django.db import models
from organizations.models import Organization


class Property(models.Model):

    PROPERTY_TYPES = [
        ("Casa", "Casas"),
        ("Apartamento", "Apartamentos"),
        ("Aparta estudio", "Aparta estudios"),
        ("Oficina", "Oficina"),
        ("Bodega", "Bodega"),
        ("Local", "Locales"),
    ]

    class DocumentType(models.TextChoices):
        CC = "CC", "Cédula de Ciudadanía"
        CE = "CE", "Cédula de Extranjería"
        NIT = "NIT", "Número de Identificación Tributaria"
        PPT = "PPT", "Permiso por Protección Temporal"
        PASAPORTE = "PASAPORTE", "Pasaporte"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    name = models.CharField(max_length=150)

    address = models.CharField(max_length=255)

    property_number = models.CharField(
        max_length=100,
        verbose_name="Número de contrato",
    )

    tenant_name = models.CharField(
        max_length=150,
        verbose_name="Nombres y apellidos del arrendatario",
    )

    document_type = models.CharField(
        max_length=15,
        choices=DocumentType.choices,
        blank=True,
    )

    document_number = models.CharField(
        max_length=50,
    )

    tenant_email = models.EmailField(
        max_length=254,
    )

    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPES,
    )

    photo_public_id = models.CharField(max_length=255, blank=True)

    photo_url = models.URLField(max_length=500, blank=True)

    created_at = models.DateField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.property_number}"

    @property
    def document_label(self):
        """
        Retorna el documento con su tipo, por ejemplo
        "Cédula de Ciudadanía 123456789". Si no hay tipo,
        solo el número.
        """
        if self.document_type and self.document_number:
            return (
                f"{self.get_document_type_display()} "
                f"{self.document_number}"
            )

        return self.document_number