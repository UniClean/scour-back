from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class ShortInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['name']

class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['name', 'cost']