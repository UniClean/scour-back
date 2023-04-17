from rest_framework import serializers
from .models import Order, CleaningOrderStatus, CleaningOrderType, OrderEmployee, OrderAttachment, OrderAttachmentEvidence
from objects.serializers import ObjectSerializer
from enumchoicefield import EnumChoiceField
from employees.serializers import ShortEmployeeSerializer


class OrderAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAttachment
        fields = ('id', 'created_at')

class OrderAttachmentEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAttachmentEvidence
        fields = ('id', 'created_at')

class OrderSerializer(serializers.ModelSerializer):
    object = ObjectSerializer(source='object_id', many=False, read_only=True)
    type = EnumChoiceField(enum_class=CleaningOrderType)
    status = EnumChoiceField(enum_class=CleaningOrderStatus)

    class Meta:
        model = Order
        fields = ['id', 'object', 'type', 'status', 'additional_information',
                  'supervisor_comments', 'report_deadline',
                  'order_attachments_ids', 'order_attachment_evidences_ids',
                    'expiration_deadline', 'confirmed_time', 'start_time',
                    'completed_time', 'created', 'updated', 'deleted', 'deleted_date',
                  ]
        depth = 1


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['object_id', 'type', 'additional_information', 'report_deadline', 'expiration_deadline']


class OrderAssignEmployeesSerializer(serializers.ModelSerializer):
    employeeIds = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Order
        fields = ['employeeIds']


class OrderAddSupervisorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['supervisor_comments']


class OrderEmployeeSerializer(serializers.ModelSerializer):
    employee = ShortEmployeeSerializer(source='employee_id', many=False, read_only=True)
    class Meta:
        model = OrderEmployee
        fields = ['id', 'employee', 'worked_hours_amount']


class OrderEmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEmployee
        fields = ['order_id','employee_id', 'worked_hours_amount']


class OrderEmployeeCreateListSerializer(serializers.ModelSerializer):
    employees = OrderEmployeeCreateSerializer(many=True)

    class Meta:
        model = OrderEmployee
        fields = ['employees']

class GetOrdersByStatusSerializer(serializers.ModelSerializer):
    status = EnumChoiceField(enum_class=CleaningOrderStatus)
    class Meta:
        model = Order
        fields = ['status']