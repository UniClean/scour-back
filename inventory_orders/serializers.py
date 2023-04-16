from rest_framework import serializers
from .models import InventoryOrder, InventoryOrderStatus, InventoryOrderItem
from objects.serializers import RequiredObjectInventorySerializer, ShortObjectSerializer
from enumchoicefield import EnumChoiceField


class InventoryOrderSerializer(serializers.ModelSerializer):
    status = EnumChoiceField(enum_class=InventoryOrderStatus)
    object = ShortObjectSerializer(source='object_id', many=False, read_only=True)

    class Meta:
        model = InventoryOrder
        fields = '__all__'


class InventoryOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryOrder
        fields = ['deadline', 'object_id']


class InventoryOrderItemSerializer(serializers.ModelSerializer):
    required_object_inventory = RequiredObjectInventorySerializer(source='required_object_inventory_id', many=False, read_only=True)

    class Meta:
        model = InventoryOrderItem
        fields = '__all__'


class InventoryOrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryOrderItem
        fields = ['inventory_order_id', 'required_object_inventory_id', 'amount']


class InventoryOrderItemCreateListSerializer(serializers.ModelSerializer):
    inventory_order_items = InventoryOrderItemCreateSerializer(many=True)

    class Meta:
        model = InventoryOrderItem
        fields = ['inventory_order_items']