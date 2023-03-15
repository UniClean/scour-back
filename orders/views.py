from django.shortcuts import render

from rest_framework import generics
from .serializers import OrderSerializer, OrderCreateSerializer
from .models import Order, CleaningOrderStatus
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View


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


class CompleteOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.status == CleaningOrderStatus.IN_PROGRESS.name:
            order.status = CleaningOrderStatus.COMPLETED.name
            order.save()
            return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Order status can only be updated to completed when status is INPROGRESS.'})


class ConfirmOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.status == CleaningOrderStatus.COMPLETED.name:
            order.status = CleaningOrderStatus.CONFIRMED.name
            order.save()
            return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Order status can only be updated to completed when status is COMPLETED.'})


class StartOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.status == CleaningOrderStatus.PLANNED.name:
            order.status = CleaningOrderStatus.IN_PROGRESS.name
            order.save()
            return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Order status can only be updated to completed when status is PLANNED.'})


class DeclineOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.status = CleaningOrderStatus.DECLINED.name
        order.save()
        return JsonResponse({'status': 'success', 'message': 'Order status has been updated to completed.'})

