from django.shortcuts import render

from rest_framework import generics
from .serializers import OrderSerializer, OrderCreateSerializer
from .models import Order, CleaningOrderStatus
from rest_framework.response import Response
from rest_framework import status


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
