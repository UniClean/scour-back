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
    path('orders/<int:order_id>/assign-employees/', views.assign_employees_to_order, name='order-assign-employees'),
    path('orders/<int:order_id>/assigned_employees', views.OrderEmployeeList.as_view(), name='order_employee'),
    path('orders/<int:order_id>/update-supervisor-comments/', views.update_supervisor_comments, name='order-assign-vehicles'),
    path('orders/status/<str:status>/', views.OrderListByStatus.as_view(), name='order_list_by_status'),
]