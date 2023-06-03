from rest_framework import generics
from .serializers import EmployeeSerializer, EmployeeCreateSerializer, PositionSerializer, PositionCreateSerializer
from .models import Employee, Position
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.filter(deleted=False)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeSerializer
        elif self.request.method == 'POST':
            return EmployeeCreateSerializer
        else:
            return EmployeeSerializer

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

class EmployeeListByPosition(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, position_id):
        employees = Employee.objects.filter(position_id=position_id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'


class EmployeeUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    lookup_field = 'id'


class EmployeeDestroy(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    lookup_field = 'id'


class PositionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Position.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PositionSerializer
        elif self.request.method == 'POST':
            return PositionCreateSerializer
        else:
            return PositionSerializer

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


class PositionDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    lookup_field = 'id'


class PositionUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Position.objects.all()
    serializer_class = PositionCreateSerializer
    lookup_field = 'id'


class PositionDestroy(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Position.objects.all()
    lookup_field = 'id'
