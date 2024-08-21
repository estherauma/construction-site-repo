from django import forms
from .models import  Worker, Attendance,Material,MaterialUsage
from django.forms import ModelForm



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

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['worker', 'date', 'time_in', 'time_out', 'daily_rate']
    
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        
        self.fields['worker'].queryset = Worker.objects.all()