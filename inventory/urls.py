from django.urls import path

import inventory.views as views

urlpatterns = [
    path('inventory/', views.InventoryList.as_view()),
    path('inventory/<int:id>/', views.InventoryDetail.as_view(), name='inventory-retrieve'),
    path('inventory/<int:id>/update/', views.InventoryUpdate.as_view(), name='inventory-update'),
    path('inventory/<int:id>/delete/', views.InventoryDestroy.as_view(), name='inventory-destroy'),
]