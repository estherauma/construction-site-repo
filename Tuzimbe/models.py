from django.db import models

# Create your models here.
class Worker(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False,unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False,unique=True)
    password = models.CharField(max_length=128, null=False, blank=False,default='password')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
