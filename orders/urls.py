from django.urls import path

import orders.views as views

urlpatterns = [
    path('orders/', views.OrderList.as_view()),
    path('orders/<int:id>/', views.OrderDetail.as_view(), name='order_detail'),
    path('orders/<int:id>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('orders/<int:id>/delete/', views.OrderDestroy.as_view(), name='order-destroy'),
    path('orders/<int:id>/start/', views.StartOrderView.as_view(), name='order-start'),
    path('orders/<int:id>/complete/', views.CompleteOrderView.as_view(), name='order-complete'),
    path('orders/<int:id>/confirm/', views.ConfirmOrderView.as_view(), name='order-confirm'),
    path('orders/<int:id>/decline/', views.DeclineOrderView.as_view(), name='order-decline'),
]