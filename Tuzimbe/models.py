from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

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