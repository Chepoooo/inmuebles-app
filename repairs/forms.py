from django import forms
from .models import Repair


class RepairForm(forms.ModelForm):

    class Meta:
        model = Repair

        fields = (
            "property",
            "repair_type",
            "report_date",
            "assigned_worker",
            "quote",
            "description",
            "status",
        )

        labels = {
            "property": "Propiedad",
            "repair_type": "Tipo de reparación",
            "report_date": "Fecha de reporte",
            "assigned_worker": "Trabajador asignado",
            "quote": "Cotización",
            "description": "Descripción",
            "status": "Estado",
        }

        widgets = {
            "report_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "assigned_worker": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del trabajador",
                }
            ),

            "quote": forms.NumberInput(
                attrs={
                    "placeholder": "Ej. 1500000",
                    "min": "0",
                    "step": "1000",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Descripción de la reparación...",
                }
            ),

            "status": forms.Select(),
        }


class InventoryRepairForm(forms.ModelForm):

    class Meta:
        model = Repair

        fields = (
            "report_date",
            "assigned_worker",
            "quote",
            "description",
            "status",
        )

        labels = {
            "report_date": "Fecha de reporte",
            "assigned_worker": "Trabajador asignado",
            "quote": "Cotización",
            "description": "Descripción",
            "status": "Estado",
        }

        widgets = {
            "report_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "assigned_worker": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del trabajador",
                }
            ),

            "quote": forms.NumberInput(
                attrs={
                    "placeholder": "Ej. 1500000",
                    "min": "0",
                    "step": "1000",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Descripción de la reparación...",
                }
            ),

            "status": forms.Select(),
        }


class RepairUserForm(forms.ModelForm):

    class Meta:
        model = Repair

        fields = (
            "status",
            "description",
        )

        labels = {
            "status": "Estado",
            "description": "Descripción",
        }

        widgets = {
            "status": forms.Select(),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Descripción de la reparación...",
                }
            ),
        }