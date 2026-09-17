from django import forms

from .models import Inventory, InventoryItem, InventorySection


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            "inventory_type",
        )
        
class InventorySectionForm(forms.ModelForm):
    class Meta:
        model = InventorySection
        fields = ("name",)
        labels = {
            "name": "Nombre de la sección",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Cochera, Terraza, Estudio...",
                }
            ),
        }



class InventoryItemForm(forms.ModelForm):

    class Meta:
        model = InventoryItem
        fields = (
            "name",
            "item_type",
            "status",
            "description",
        )

        labels = {
            "name": "Nombre",
            "item_type": "Tipo o material",
            "status": "Estado",
            "description": "Descripción",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Puerta, Ventana, Piso...",
                }
            ),
            "item_type": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Madera, Aluminio, Cerámica...",
                }
            ),
            "status": forms.Select(),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Descripción u observación...",
                }
            ),
        }

    def clean_status(self):
        status = self.cleaned_data.get("status")

        if not status:
            raise forms.ValidationError(
                "Debe seleccionar el estado."
            )

        return status