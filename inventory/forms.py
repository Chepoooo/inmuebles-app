from django import forms

from .models import Inventory, InventoryItem


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            "inventory_type",
        )


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = (
            "name",
            "description",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }