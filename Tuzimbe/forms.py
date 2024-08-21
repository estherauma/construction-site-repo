from django.forms import ModelForm
from .models import Worker, Attendance
from django import forms

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