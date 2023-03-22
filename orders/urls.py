from django.urls import path

import orders.views as views

urlpatterns = [
    path('orders/', views.OrderList.as_view()),
    path('orders/<int:id>/', views.OrderDetail.as_view(), name='order_detail'),
    path('orders/<int:id>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('orders/<int:id>/delete/', views.OrderDestroy.as_view(), name='order-destroy'),
    path('orders/<int:order_id>/start/', views.start_order, name='order-start'),
    path('orders/<int:order_id>/complete/', views.complete_order, name='order-complete'),
    path('orders/<int:order_id>/confirm/', views.confirm_order, name='order-confirm'),
    path('orders/<int:order_id>/decline/', views.decline_order, name='order-decline'),
    path('orders/<int:order_id>/assign-employees/', views.assign_employees, name='order-assign-employees'),
]