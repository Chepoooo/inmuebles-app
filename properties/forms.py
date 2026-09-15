from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):

    photo = forms.ImageField(
        required=False,
        label="Foto de la propiedad",
    )

    class Meta:
        model = Property
        fields = (
            "name",
            "address",
            "property_number",
            "tenant_name",
            "document_number",
            "tenant_email",
            "created_at",
            "property_type",
        )
        labels = {
            "name": "Nombre de la propiedad",
            "address": "Dirección",
            "property_number": "Número de propiedad",
            "tenant_name": "Arrendatario",
            "document_number": "Número de documento",
            "tenant_email": "Correo electrónico",
            "created_at": "Fecha de creación",
            "property_type": "Tipo de inmueble",
        }
        widgets = {
            "document_number": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "pattern": "[0-9]*",
                },
            ),
            "created_at": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
        }
        error_messages = {
            "name": {
                "required": "El nombre de la propiedad es obligatorio.",
            },
            "address": {
                "required": "La dirección es obligatoria.",
            },
            "property_number": {
                "required": "El número de propiedad es obligatorio.",
            },
            "tenant_name": {
                "required": "El nombre y apellido del arrendatario son obligatorios.",
            },
            "document_number": {
                "required": "El número de documento es obligatorio.",
            },
            "tenant_email": {
                "required": "El correo electrónico es obligatorio.",
                "invalid": "Ingrese un correo electrónico válido.",
            },
            "created_at": {
                "required": "La fecha de creación es obligatoria.",
                "invalid": "Ingrese una fecha válida.",
            },
            "property_type": {
                "required": "El tipo de inmueble es obligatorio.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["created_at"].input_formats = ["%Y-%m-%d"]

        self.fields["document_number"].required = True
        self.fields["tenant_email"].required = True
        self.fields["property_type"].required = True
        self.fields["created_at"].required = True

    def clean_tenant_name(self):
        tenant_name = self.cleaned_data["tenant_name"].strip()

        parts = tenant_name.split()

        if len(parts) < 2:
            raise forms.ValidationError(
                "Ingrese el nombre y apellido del arrendatario."
            )

        if not all(part.isalpha() for part in parts):
            raise forms.ValidationError(
                "El nombre del arrendatario solo puede contener letras."
            )

        return tenant_name

    def clean_document_number(self):
        document_number = self.cleaned_data["document_number"].strip()

        if not document_number.isdigit():
            raise forms.ValidationError(
                "El número de documento solo puede contener números."
            )

        return document_number