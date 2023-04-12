from rest_framework import serializers
from .models import Employee, Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ShortPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']


class PositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']


class EmployeeSerializer(serializers.ModelSerializer):
    position = ShortPositionSerializer(source='position_id', many=False, read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'


class ShortEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'surname', 'phone', 'email']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'surname', 'position_id', 'phone', 'email', 'date_of_birth',
                  'date_of_employment', 'salary', 'rate', 'address', 'city']



