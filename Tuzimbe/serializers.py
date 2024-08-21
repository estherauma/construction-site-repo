from .models import Material
from rest_framework import serializers

class  MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name',  'total_quantity_stocked','unit', 'price_per_unit']
