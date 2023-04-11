from django.urls import path

import objects.views as views

urlpatterns = [
    path('objects/', views.ObjectList.as_view()),
    path('objects/<int:id>/', views.ObjectDetail.as_view(), name='object-retrieve'),
    path('objects/<int:id>/update/', views.ObjectUpdate.as_view(), name='object-update'),
    path('objects/<int:id>/delete/', views.ObjectDestroy.as_view(), name='object-destroy'),

    path('required-object-inventory/', views.RequiredObjectInventoryList.as_view()),
    path('required-object-inventory/object/<int:object_id>/', views.RequiredObjectInventoryListByObjectId.as_view(), name='required-object-inventory-by-object-id'),
    path('required-object-inventory/create-several/', views.add_required_object_inventories, name='add-several-required-object-inventories'),
    path('required-object-inventory/<int:id>/', views.RequiredObjectInventoryDetail.as_view(), name='required-object-inventory-retrieve'),
    path('required-object-inventory/<int:id>/update/', views.RequiredObjectInventoryUpdate.as_view(), name='required-object-inventory-update'),
    path('required-object-inventory/<int:id>/delete/', views.RequiredObjectInventoryDestroy.as_view(), name='required-object-inventory-destroy'),

]