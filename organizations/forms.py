from django import forms

from .models import Organization


class OrganizationSettingsForm(forms.ModelForm):

    logo = forms.FileField(
        required=False,
        label="Logo de la organización",
    )

    class Meta:
        model = Organization
        fields = [
            "name",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": (
                        "Nombre de la organización"
                    ),
                }
            ),
        }

        labels = {
            "name": "Nombre de la organización",
        }

        help_texts = {
            "name": (
                "Este nombre aparecerá en los "
                "documentos PDF de la organización."
            ),
        }