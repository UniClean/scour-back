from rest_framework import generics
from .serializers import ObjectSerializer, ObjectCreateSerializer, RequiredObjectInventorySerializer, \
    RequiredObjectInventoryCreateSerializer, RequiredObjectInventoryCreateListSerializer
from .models import Object, RequiredObjectInventory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse


class ObjectList(generics.ListCreateAPIView):
    queryset = Object.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ObjectSerializer
        elif self.request.method == 'POST':
            return ObjectCreateSerializer
        else:
            return ObjectSerializer

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


class ObjectDetail(generics.RetrieveAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    lookup_field = 'id'


class ObjectUpdate(generics.UpdateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectCreateSerializer
    lookup_field = 'id'


class ObjectDestroy(generics.DestroyAPIView):
    queryset = Object.objects.all()
    lookup_field = 'id'


class RequiredObjectInventoryList(generics.ListCreateAPIView):
    queryset = RequiredObjectInventory.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RequiredObjectInventorySerializer
        elif self.request.method == 'POST':
            return RequiredObjectInventoryCreateSerializer
        else:
            return RequiredObjectInventorySerializer

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


class RequiredObjectInventoryListByObjectId(generics.ListAPIView):
    queryset = RequiredObjectInventory.objects.all()
    serializer_class = RequiredObjectInventorySerializer
    def get_queryset(self, *args, **kwargs):
        object_id = self.kwargs['object_id']
        queryset = RequiredObjectInventory.objects.filter(object_id_id=object_id)
        return queryset

@swagger_auto_schema(method='post', request_body=RequiredObjectInventoryCreateListSerializer)
@api_view(['POST'])
def add_required_object_inventories(request):
    required_object_inventories = request.data.get('required_object_inventories', [])
    serializer = RequiredObjectInventoryCreateSerializer(data=required_object_inventories, many=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success', 'message': 'Required object inventories added successfully'})
    return JsonResponse({'status': 'error', 'message': serializer.errors})


class RequiredObjectInventoryDetail(generics.RetrieveAPIView):
    queryset = RequiredObjectInventory.objects.all()
    serializer_class = RequiredObjectInventorySerializer
    lookup_field = 'id'


class RequiredObjectInventoryUpdate(generics.UpdateAPIView):
    queryset = RequiredObjectInventory.objects.all()
    serializer_class = RequiredObjectInventoryCreateSerializer
    lookup_field = 'id'


class RequiredObjectInventoryDestroy(generics.DestroyAPIView):
    queryset = RequiredObjectInventory.objects.all()
    lookup_field = 'id'
