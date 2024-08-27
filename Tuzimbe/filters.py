import django_filters
from .models import MaterialUsage


class MaterialUsageFilter(django_filters.FilterSet):
    material_name = django_filters.CharFilter(field_name='material', lookup_expr='icontains')
    date_used = django_filters.DateFromToRangeFilter(field_name='date', label="Date range")

    class Meta:
        model = MaterialUsage
        fields = ['material', 'date']
    