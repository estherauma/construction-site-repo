from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.utils import timezone
def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')


# Create your models here.
class Worker(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False,unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False,unique=True)
    password = models.CharField(max_length=128, null=False, blank=False,default='password')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, validators=[validate_not_future_date])
    time_in = models.TimeField(default=timezone.now)
    time_out = models.TimeField(default=timezone.now)
    daily_rate= models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def clean(self):
        super().clean()
        if self.daily_rate < 0:
            raise ValidationError({'daily_rate': 'Daily rate cannot be negative.'})
        
        now = timezone.now().time()
        if self.time_in > now:
            raise ValidationError({'time_in': 'Time in cannot be in the future.'})
        
        if self.time_out > now:
            raise ValidationError({'time_out': 'Time out cannot be in the future.'})

        if self.time_out < self.time_in:
            raise ValidationError({'time_out': 'Time out must be after time in.'})

    def __str__(self):
        return f"{self.worker.first_name} {self.worker.last_name} {self.date}"

