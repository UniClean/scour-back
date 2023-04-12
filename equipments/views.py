from rest_framework import generics
from .serializers import EquipmentSerializer, EquipmentCreateSerializer, EquipmentAssignObjectSerializer
from .models import Equipment
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.http import JsonResponse
from objects import models as object_models


class EquipmentList(generics.ListCreateAPIView):
    queryset = Equipment.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EquipmentSerializer
        elif self.request.method == 'POST':
            return EquipmentCreateSerializer
        else:
            return EquipmentSerializer

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


class EquipmentListByObjectId(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    def get_queryset(self, *args, **kwargs):
        object_id = self.kwargs['object_id']
        queryset = Equipment.objects.filter(object_id_id=object_id)
        return queryset


class EquipmentDetail(generics.RetrieveAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    lookup_field = 'id'


class EquipmentUpdate(generics.UpdateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentCreateSerializer
    lookup_field = 'id'


class EquipmentDestroy(generics.DestroyAPIView):
    queryset = Equipment.objects.all()
    lookup_field = 'id'


@swagger_auto_schema(method='post', request_body=EquipmentAssignObjectSerializer)
@api_view(['POST'])
def assign_object(request, id):
    try:
        equipment = Equipment.objects.get(pk=id)
    except Equipment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Equipment not found.'})

    try:
        object_id = request.data.get('objectId')
        assigned_object = object_models.Object.objects.get(pk=object_id)
    except object_models.Object.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Object not found.'})

    equipment.object_id = assigned_object
    equipment.save()
    return JsonResponse({'status': 'success', 'message': 'Equipment have been assigned to the object.'})
