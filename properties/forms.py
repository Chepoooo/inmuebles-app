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
        )

        labels = {
            "name": "Nombre de la propiedad",
            "address": "Dirección",
            "property_number": "Número de propiedad",
            "tenant_name": "Nombre del inquilino",
        }