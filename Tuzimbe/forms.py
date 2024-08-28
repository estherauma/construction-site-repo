from django import forms
from .models import  Worker, Attendance,Material,MaterialUsage
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        min_length = 8
        if len(password) < min_length:
            raise forms.ValidationError(f"Password must be at least {min_length} characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")

        return password


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

  