from rest_framework import generics
from .serializers import CustomerSerializer, CustomerCreateSerializer,CustomerContractFileSerializer
from .models import Customer, CustomerContract
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import status
from django.utils import timezone
from django.http import HttpResponse


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


class CustomerContractUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        if 'customer_id' not in request.data:
            raise ParseError("Customer id not provided")
        customer_id = request.data['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        f = request.data['file']
        f.name = str(customer.id)+ "_" + timezone.now().strftime("%Y%m%d%H%M%S") + "_" + f.name
        customer_contract = CustomerContract(customer_id=customer, contract_file=f)
        customer_contract.save()
        return Response(status=status.HTTP_201_CREATED)


class CustomerContractDetail(generics.RetrieveAPIView):
    queryset = CustomerContract.objects.all()
    serializer_class = CustomerContractFileSerializer
    lookup_field = 'id'

def get_contract_file_content(request, id):
    file = CustomerContract.objects.get(id=id).contract_file
    file_content = get_file_content(file)
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'

    return response

def get_file_content(file):
    with file.open('rb') as f:
        file_content = f.read()
    return file_content