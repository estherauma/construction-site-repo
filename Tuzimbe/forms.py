from django import forms
from .models import Material, MaterialUsage


class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit', 'total_quantity_stocked', 'price_per_unit']

class UsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = ['material', 'date', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }