from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from .serializers import OrderSerializer, OrderCreateSerializer, OrderAssignEmployeesSerializer, \
    OrderEmployeeCreateSerializer, OrderEmployeeCreateListSerializer, OrderAddSupervisorCommentSerializer, GetOrdersByStatusSerializer
from .models import Order
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from employees import models as employee_models
from drf_yasg.utils import swagger_auto_schema
from .models import OrderEmployee, CleaningOrderStatus, OrderAttachment, OrderAttachmentEvidence
from .serializers import OrderEmployeeSerializer
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
import mimetypes

class OrderList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        elif self.request.method == 'POST':
            return OrderCreateSerializer
        else:
            return OrderSerializer

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        queryset = self.get_queryset()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response({"id": item.id, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'


class OrderUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = 'id'


class OrderDestroy(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status == CleaningOrderStatus.IN_PROGRESS:
        order.status = CleaningOrderStatus.COMPLETED
        order.completed_time = datetime.now()
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})
    return JsonResponse(
        {'status': 'error', 'message': 'Order status can only be updated to completed when status is INPROGRESS.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status == CleaningOrderStatus.COMPLETED:
        order.status = CleaningOrderStatus.CONFIRMED
        order.confirmed_time = datetime.now()
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to confirmed.'})
    return JsonResponse(
        {'status': 'error', 'message': 'Order status can only be updated to confirmed when status is COMPLETED.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status == CleaningOrderStatus.PLANNED:
        order.status = CleaningOrderStatus.IN_PROGRESS
        order.start_time = datetime.now()
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to in progress.'})
    return JsonResponse(
        {'status': 'error', 'message': 'Order status can only be updated to in progress when status is PLANNED.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = CleaningOrderStatus.DECLINED
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Order status has been updated to declined.'})


@swagger_auto_schema(method='post', request_body=OrderAssignEmployeesSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_employees(request, order_id):
    order = Order.objects.get(pk=order_id)
    employee_ids = request.data.get('employeeIds', [])
    for i in employee_ids:
        employee = employee_models.Employee.objects.get(pk=i)
        order.employees.add(employee)
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Employees have been assigned to the order.'})


@swagger_auto_schema(method='post', request_body=OrderAddSupervisorCommentSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_supervisor_comments(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.supervisor_comments = request.data.get('supervisor_comments')
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Supervisor comment has been updated.'})


@swagger_auto_schema(method='post', request_body=OrderEmployeeCreateListSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_employees_to_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Order does not exist.'})

    employees = request.data.get('employees', [])
    serializer = OrderEmployeeCreateSerializer(data=employees, many=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success', 'message': 'Employees have been assigned to the order.'})
    return JsonResponse({'status': 'error', 'message': serializer.errors})


class OrderEmployeeList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OrderEmployee.objects.all()
    serializer_class = OrderEmployeeSerializer
    def get_queryset(self, *args, **kwargs):
        order_id = self.kwargs['order_id']
        queryset = OrderEmployee.objects.filter(order_id_id=order_id)
        return queryset

class OrderListByStatus(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self, *args, **kwargs):
        status_name = self.kwargs['status']
        queryset = Order.objects.filter(status=CleaningOrderStatus[status_name], deleted=False)
        return queryset


class OrderAttachmentsUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'attachment' not in request.data:
            raise ParseError("Empty content")
        if 'order_id' not in request.data:
            raise ParseError("Order id not provided")
        order_id = request.data['order_id']
        order = Order.objects.get(pk=order_id)
        f = request.data['attachment']
        f.name = str(order.id)+ "_" + timezone.now().strftime("%Y%m%d%H%M%S") + "_" + f.name
        order_attachment = OrderAttachment(order_id=order, attachment=f)
        order_attachment.save()
        return Response(status=status.HTTP_201_CREATED)


class OrderAttachmentEvidencesUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'attachment' not in request.data:
            raise ParseError("Empty content")
        if 'order_id' not in request.data:
            raise ParseError("Order id not provided")
        order_id = request.data['order_id']
        order = Order.objects.get(pk=order_id)
        f = request.data['attachment']
        f.name = str(order.id)+ "_" + timezone.now().strftime("%Y%m%d%H%M%S") + "_" + "_evidence"+ f.name
        order_attachment = OrderAttachmentEvidence(order_id=order, attachment=f)
        order_attachment.save()
        return Response(status=status.HTTP_201_CREATED)


def get_order_attachment(request, attachment_id):
    file = OrderAttachment.objects.get(id=attachment_id).attachment
    file_content = get_file_content(file)
    response = HttpResponse(file_content, content_type=get_content_type(file.name))
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'

    return response


def get_order_attachment_evidence(request, attachment_evidence_id):
    file = OrderAttachmentEvidence.objects.get(id=attachment_evidence_id).attachment
    file_content = get_file_content(file)
    response = HttpResponse(file_content, content_type=get_content_type(file.name))
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'

    return response


def get_file_content(file):
    with file.open('rb') as f:
        file_content = f.read()
    return file_content


def get_content_type(filename):
    content_type, encoding = mimetypes.guess_type(filename)
    return content_type