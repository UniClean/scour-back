from rest_framework import serializers
from .models import Object
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