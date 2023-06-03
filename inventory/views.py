from rest_framework import generics
from .serializers import InventorySerializer, InventoryCreateSerializer
from .models import Inventory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class InventoryList(generics.ListCreateAPIView):
    queryset = Inventory.objects.filter(deleted=False)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InventorySerializer
        elif self.request.method == 'POST':
            return InventoryCreateSerializer
        else:
            return InventorySerializer

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


class InventoryDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'id'


class InventoryUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventoryCreateSerializer
    lookup_field = 'id'


class InventoryDestroy(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.all()
    lookup_field = 'id'
