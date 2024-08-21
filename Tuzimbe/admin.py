from django.contrib import admin
from .models import Material, MaterialUsage

# Register your models here.
admin.site.register(Material)
admin.site.register(MaterialUsage)