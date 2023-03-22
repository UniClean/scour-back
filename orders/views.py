from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import OrderSerializer, OrderCreateSerializer, OrderAssignEmployeesSerializer
from .models import Order, CleaningOrderStatus
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from employees import models as employee_models
from drf_yasg.utils import swagger_auto_schema


class OrderList(generics.ListCreateAPIView):
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'


class OrderUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    lookup_field = 'id'


class OrderDestroy(generics.DestroyAPIView):
    queryset = Order.objects.all()
    lookup_field = 'id'

@api_view(['POST'])
def complete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status == CleaningOrderStatus.IN_PROGRESS:
        order.status = CleaningOrderStatus.COMPLETED
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})
    return JsonResponse({'status': 'error', 'message': 'Order status can only be updated to completed when status is INPROGRESS.'})

@api_view(['POST'])
def confirm_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status == CleaningOrderStatus.COMPLETED:
        order.status = CleaningOrderStatus.CONFIRMED
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to confirmed.'})
    return JsonResponse({'status': 'error', 'message': 'Order status can only be updated to confirmed when status is COMPLETED.'})

@api_view(['POST'])
def start_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status == CleaningOrderStatus.PLANNED:
        order.status = CleaningOrderStatus.IN_PROGRESS
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to in progress.'})
    return JsonResponse({'status': 'error', 'message': 'Order status can only be updated to in progress when status is PLANNED.'})

@api_view(['POST'])
def decline_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = CleaningOrderStatus.DECLINED
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Order status has been updated to declined.'})


@swagger_auto_schema(method='post', request_body=OrderAssignEmployeesSerializer)
@api_view(['POST'])
def assign_employees(request, order_id):
    order = Order.objects.get(pk=order_id)
    employee_ids = request.data.get('employee_ids', [])
    for i in employee_ids:
        employee = employee_models.Employee.objects.get(pk=i)
        order.employees.add(employee)
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Employees have been assigned to the order.'})

