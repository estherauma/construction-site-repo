from django.contrib import admin
# from .models import Material, MaterialUsage
from .models import Worker,Attendance,AggregatedData

# Register your models here.
admin.site.register(Worker)
admin.site.register(Attendance)
admin.site.register(AggregatedData)