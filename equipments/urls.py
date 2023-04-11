from django.urls import path

import equipments.views as views

urlpatterns = [
    path('equipments/', views.EquipmentList.as_view()),
    path('equipments/object/<int:object_id>/', views.EquipmentListByObjectId.as_view(), name='equipment-list-by-object-id'),
    path('equipments/<int:id>/', views.EquipmentDetail.as_view(), name='equipment-retrieve'),
    path('equipments/<int:id>/update/', views.EquipmentUpdate.as_view(), name='equipment-update'),
    path('equipments/<int:id>/delete/', views.EquipmentDestroy.as_view(), name='equipment-destroy'),
    path('equipments/<int:id>/assign_object/', views.assign_object, name='object-to-equipment-assign'),
]