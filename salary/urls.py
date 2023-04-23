from django.urls import path

import salary.views as views

urlpatterns = [
    path('salary/<int:employee_id>/<int:month>/<int:year>/', views.EmployeeSalaryListByMonth.as_view()),
path('salary/all_employees/<int:month>/<int:year>/', views.SalaryListByMonth.as_view()),
    path('salary/change_paid_status/', views.change_paid_status),
]