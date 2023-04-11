from rest_framework import serializers
from .models import Equipment
from objects.serializers import ShortObjectSerializer


class EquipmentSerializer(serializers.ModelSerializer):
    object = ShortObjectSerializer(source='object_id', many=False, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'


class EquipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name', 'cost', 'object_id']


class EquipmentAssignObjectSerializer(serializers.ModelSerializer):
    objectId = serializers.IntegerField()

    class Meta:
        model = Equipment
        fields = ['objectId']