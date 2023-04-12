from rest_framework import generics
from .serializers import CustomerSerializer, CustomerCreateSerializer
from .models import Customer
from rest_framework.response import Response
from rest_framework import status


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerSerializer
        elif self.request.method == 'POST':
            return CustomerCreateSerializer
        else:
            return CustomerSerializer

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


class CustomerDetail(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'


class CustomerUpdate(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
    lookup_field = 'id'


class CustomerDestroy(generics.DestroyAPIView):
    queryset = Customer.objects.all()
    lookup_field = 'id'
