from rest_framework import serializers
from employees.serializers import ShortEmployeeSerializer
from orders.models import OrderEmployee


class OrderEmployeeSalariesSerializer(serializers.ModelSerializer):
    employee = ShortEmployeeSerializer(source='employee_id', many=False, read_only=True)
    class Meta:
        model = OrderEmployee
        fields = ['id', 'employee', 'worked_hours_amount', 'is_paid', 'object_name', 'payout_per_order', 'employee_base_rate']


class OrderEmployeeSalariesChangePaidToTrueStatusSerializer(serializers.ModelSerializer):
    employee_salary_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = OrderEmployee
        fields = ['employee_salary_ids']