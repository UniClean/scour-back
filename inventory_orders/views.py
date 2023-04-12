from rest_framework import generics
from .serializers import InventoryOrderSerializer, InventoryOrderCreateSerializer, InventoryOrderItemSerializer, \
    InventoryOrderItemCreateSerializer, InventoryOrderItemCreateListSerializer
from .models import InventoryOrder, InventoryOrderItem, InventoryOrderStatus
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from datetime import datetime


class InventoryOrderList(generics.ListCreateAPIView):
    queryset = InventoryOrder.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InventoryOrderSerializer
        elif self.request.method == 'POST':
            return InventoryOrderCreateSerializer
        else:
            return InventoryOrderSerializer

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


class InventoryOrderDetail(generics.RetrieveAPIView):
    queryset = InventoryOrder.objects.all()
    serializer_class = InventoryOrderSerializer
    lookup_field = 'id'


class InventoryOrderUpdate(generics.UpdateAPIView):
    queryset = InventoryOrder.objects.all()
    serializer_class = InventoryOrderCreateSerializer
    lookup_field = 'id'


class InventoryOrderDestroy(generics.DestroyAPIView):
    queryset = InventoryOrder.objects.all()
    lookup_field = 'id'

@api_view(['POST'])
def start_order(request, order_id):
    order = InventoryOrder.objects.get(pk=order_id)
    if order.status == InventoryOrderStatus.CREATED:
        order.status = InventoryOrderStatus.IN_PROGRESS
        order.in_progress_time = datetime.now()
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to in progress.'})
    return JsonResponse(
        {'status': 'error', 'message': 'Order status can only be updated to IN_PROGRESS when status is CREATED.'})


@api_view(['POST'])
def complete_order(request, order_id):
    order = InventoryOrder.objects.get(pk=order_id)
    if order.status == InventoryOrderStatus.IN_PROGRESS:
        order.status = InventoryOrderStatus.COMPLETED
        order.completed_time = datetime.now()
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})
    return JsonResponse(
        {'status': 'error', 'message': 'Order status can only be updated to COMPLETED when status is IN_PROGRESS.'})


@api_view(['POST'])
def decline_order(request, order_id):
    order = InventoryOrder.objects.get(pk=order_id)
    order.status = InventoryOrderStatus.DECLINED
    order.save()
    return JsonResponse({'status': 'success', 'message': 'Order status has been updated to declined.'})


class InventoryOrderItemListByOrderId(generics.ListAPIView):
    queryset = InventoryOrderItem.objects.all()
    serializer_class = InventoryOrderItemSerializer
    def get_queryset(self, *args, **kwargs):
        order_id = self.kwargs['order_id']
        queryset = InventoryOrderItem.objects.filter(inventory_order_id_id=order_id)
        return queryset


@swagger_auto_schema(method='post', request_body=InventoryOrderItemCreateListSerializer)
@api_view(['POST'])
def add_inventory_order_items(request):
    inventory_order_items = request.data.get('inventory_order_items', [])
    serializer = InventoryOrderItemCreateSerializer(data=inventory_order_items, many=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success', 'message': 'Inventory order items created successfully'})
    return JsonResponse({'status': 'error', 'message': serializer.errors})


class InventoryOrderItemDetail(generics.RetrieveAPIView):
    queryset = InventoryOrderItem.objects.all()
    serializer_class = InventoryOrderItemSerializer
    lookup_field = 'id'


class InventoryOrderItemUpdate(generics.UpdateAPIView):
    queryset = InventoryOrderItem.objects.all()
    serializer_class = InventoryOrderItemCreateSerializer
    lookup_field = 'id'


class RequiredObjectInventoryDestroy(generics.DestroyAPIView):
    queryset = InventoryOrderItem.objects.all()
    lookup_field = 'id'

