from rest_framework import serializers
from .models import Customer, CustomerContract


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ShortCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'is_vip']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'is_vip', 'additional_information', 'image_url', 'email', 'website', 'phone_number']


class CustomerContractFileUploadSerializer(serializers.ModelSerializer):
    contract_file = serializers.FileField()
    class Meta:
        model = CustomerContract
        fields = ['customer_id', 'contract_file']


class CustomerContractFileSerializer(serializers.ModelSerializer):
    customer = ShortCustomerSerializer(source='customer_id', many=False, read_only=True)
    contract_file_url = serializers.SerializerMethodField()
    class Meta:
        model = CustomerContract
        fields = ['customer_id', 'customer', 'contract_file', 'contract_file_url', 'created', 'updated', 'deleted', 'deleted_date']

    def get_contract_file_url(self, obj):
        return obj.contract_file.url
