from rest_framework import serializers
from .models import Employee, Position


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'surname', 'position_id', 'phone', 'email', 'date_of_birth',
                  'date_of_employment', 'salary', 'address', 'city']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class PositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']
