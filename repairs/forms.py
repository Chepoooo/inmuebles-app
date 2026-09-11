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
        widgets = {
            "report_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }
        
class RepairUserForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = (
            "status",
            "description",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }