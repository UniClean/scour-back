from django.urls import path

import employees.views as views

urlpatterns = [
    path('employees/', views.EmployeeList.as_view()),
    path('employees/position/<int:position_id>/', views.EmployeeListByPosition.as_view()),
    path('employees/<int:id>/', views.EmployeeDetail.as_view(), name='employee-retrieve'),
    path('employees/<int:id>/update/', views.EmployeeUpdate.as_view(), name='employee-update'),
    path('employees/<int:id>/delete/', views.EmployeeDestroy.as_view(), name='employee-destroy'),
    path('position/', views.PositionList.as_view()),
    path('position/<int:id>/', views.PositionDetail.as_view(), name='position-retrieve'),
    path('position/<int:id>/update/', views.PositionUpdate.as_view(), name='position-update'),
    path('position/<int:id>/delete/', views.PositionDestroy.as_view(), name='position-destroy'),
]