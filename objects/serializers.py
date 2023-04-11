from rest_framework import serializers
from .models import Object, RequiredObjectInventory
from employees.serializers import ShortEmployeeSerializer
from customers.serializers import ShortCustomerSerializer


class ObjectSerializer(serializers.ModelSerializer):
    assigned_supervisor = ShortEmployeeSerializer(source='assigned_supervisor_id', many=False, read_only=True)
    customer = ShortCustomerSerializer(source='customer_id', many=False, read_only=True)

    class Meta:
        model = Object
        fields = '__all__'


class ShortObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ['id', 'name', 'address']


class ObjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ['customer_id', 'assigned_supervisor_id', 'name', 'address', 'area', 'object_image_url', 'additional_information',
                  'required_worker_amount']


class RequiredObjectInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredObjectInventory
        fields = '__all__'


class RequiredObjectInventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredObjectInventory
        fields = ['object_id', 'inventory_id', 'amount']

class RequiredObjectInventoryCreateListSerializer(serializers.ModelSerializer):
    required_object_inventories = RequiredObjectInventoryCreateSerializer(many=True)

    class Meta:
        model = RequiredObjectInventory
        fields = ['required_object_inventories']


