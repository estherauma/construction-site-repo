from .models import Worker
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        worker = Worker.objects.create(**validated_data)
        return worker


