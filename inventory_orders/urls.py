from django.urls import path

import inventory_orders.views as views

urlpatterns = [
    path('inventory-orders/', views.InventoryOrderList.as_view()),
    path('inventory-orders/<int:id>/', views.InventoryOrderDetail.as_view(), name='object-retrieve'),
    path('inventory-orders/<int:id>/update/', views.InventoryOrderUpdate.as_view(), name='object-update'),
    path('inventory-orders/<int:id>/delete/', views.InventoryOrderDestroy.as_view(), name='object-destroy'),

    path('inventory-orders/<int:order_id>/start/', views.start_order, name='order-start'),
    path('inventory-orders/<int:order_id>/complete/', views.complete_order, name='order-complete'),
    path('inventory-orders/<int:order_id>/decline/', views.decline_order, name='order-decline'),

    path('inventory-order-item/order/<int:order_id>/', views.InventoryOrderItemListByOrderId.as_view(), name='required-object-inventory-by-object-id'),
    path('inventory-order-item/create-several/', views.add_inventory_order_items, name='add-several-required-object-inventories'),
    path('inventory-order-item/<int:id>/', views.InventoryOrderItemDetail.as_view(), name='required-object-inventory-retrieve'),
    path('inventory-order-item/<int:id>/update/', views.InventoryOrderItemUpdate.as_view(), name='required-object-inventory-update'),
    path('inventory-order-item/<int:id>/delete/', views.RequiredObjectInventoryDestroy.as_view(), name='required-object-inventory-destroy'),

]