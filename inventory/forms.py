from django import forms

from .models import (
    Inventory,
    InventoryItem,
    InventorySection,
    InventoryNote,
)


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            "inventory_type",
        )
        labels = {
            "inventory_type": "Tipo de inventario",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["inventory_type"].choices = [
            ("", "Seleccionar una opción"),
            *Inventory.InventoryType.choices,
        ]
        self.fields["inventory_type"].error_messages = {
            "required": "Debe seleccionar el tipo de inventario.",
        }
        
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


class InventoryNoteForm(forms.ModelForm):

    class Meta:
        model = InventoryNote
        fields = (
            "title",
            "content",
            "order",
        )
        labels = {
            "title": "Título",
            "content": "Contenido",
            "order": "Orden",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }