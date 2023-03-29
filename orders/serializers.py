from rest_framework import serializers
from .models import Order, CleaningOrderStatus, CleaningOrderType
from objects.serializers import ObjectSerializer
from enumchoicefield import EnumChoiceField


class OrderSerializer(serializers.ModelSerializer):
    object = ObjectSerializer(source='object_id', many=False, read_only=True)
    type = EnumChoiceField(enum_class=CleaningOrderType)
    status = EnumChoiceField(enum_class=CleaningOrderStatus)

    class Meta:
        model = Order
        exclude = ('object_id',)
        depth = 1


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['object_id', 'type', 'additional_information', 'report_deadline']


class OrderAssignEmployeesSerializer(serializers.ModelSerializer):
    employeeIds = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Order
        fields = ['employeeIds']