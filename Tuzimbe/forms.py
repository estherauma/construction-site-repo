from django.forms import ModelForm
from .models import Worker
from django import forms

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['first_name', 'last_name', 'phone_number', 'email']