from datetime import date, timedelta
from dateutil.relativedelta import relativedelta 
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')


# Create your models here.
class Material(models.Model):
    MATERIAL_UNIT_CHOICE = [
        ('KGS', 'Kilograms'),
        ('Ltrs', 'Litters'),
        ('Pcs', 'Pieces'),
        ('Cm3', 'Cubic Meters'),
        ('Tns', 'Tonnes'),
    ]
    name = models.CharField(max_length=100)
    total_quantity_stocked = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=4, choices=MATERIAL_UNIT_CHOICE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.total_quantity_stocked < 0 or self.price_per_unit < 0:
            raise ValidationError("Total quantity stocked and Price per Uint can't be negative.")
        
        existing_material = Material.objects.filter(name=self.name, unit=self.unit).first()

        if existing_material and existing_material.id != self.id:
            existing_material.total_quantity_stocked += self.total_quantity_stocked
            existing_material.total_price = existing_material.total_quantity_stocked * self.price_per_unit
            existing_material.save()
            return
        
        self.total_price = self.total_quantity_stocked * self.price_per_unit
        super().save(*args, **kwargs)
        
    def total_quantity_used(self):
        used_quantity = self.usage.aggregate(amount_used=Sum('quantity'))['amount_used'] or 0
        return used_quantity
    
    def remaining_quantity(self):
        return self.total_quantity_stocked - self.total_quantity_used()
    
    def remaining_material_cost(self):
        return self.remaining_quantity() * self.price_per_unit

    def _str__(self):
        return f"{self.name} ({str(self.total_quantity_stocked)} {self.get_unit_display()} stocked)"

    def get_total_used_quantity__for_period(self, start_date, end_date):
        usage_data = self.usage.filter(date__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('quantity'), total_cost=Sum('total_price')
        )
        return usage_data
    
    def get_daily_usage(self, date=None):
        if not date:
            date = timezone.now().date()
        return self.get_total_used_quantity__for_period(date, date)
    
    def get_weekly_usage(self, date=None):
        if not date:
            date = timezone.now().date()
        start_date = date - timedelta(days=date.weekday())
        end_date = date + timedelta(days=6)
        return self.get_total_used_quantity__for_period(start_date, end_date)
    
    def get_monthly_usage(self, year=None, month=None):
        if not year or not month:
            today = timezone.now().date()
            year = today.year
            month = today.month
        start_date = date(year, month, 1)
        end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
        return self.get_total_used_quantity__for_period(start_date, end_date)
    

class MaterialUsage(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="usage")
    date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.quantity > self.material.remaining_quantity():
            raise ValueError(f"Cannot use {self.quantity} {self.material.get_unit_display()}; only {self.material.remaining_quantity()} available.")
        
        self.total_price = self.quantity * self.material.price_per_unit
        self.material.total_quantity_stocked -= self.quantity
        self.material.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material.name} on {self.date}: {self.quantity} {self.material.get_unit_display()} were used"
    

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
        
        
    def __str__(self):
        return f"{self.worker.first_name} {self.worker.last_name} {self.date}"
    


        

