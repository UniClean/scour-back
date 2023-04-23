from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from orders.models import OrderEmployee
from .serializers import OrderEmployeeSalariesSerializer, OrderEmployeeSalariesChangePaidToTrueStatusSerializer, OrderShortEmployeeSalariesSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from employees.models import Employee
from django.db.models.functions import ExtractMonth

class EmployeeSalaryListByMonth(APIView):
    def get(self, request, employee_id, month, year):
        employee_salaries = OrderEmployee.objects.filter(employee_id=employee_id, order_id__start_time__month=month, order_id__start_time__year=year)
        serializer = OrderEmployeeSalariesSerializer(employee_salaries, many=True)
        return Response(serializer.data)

class SalaryListByMonth(APIView):
    def get(self, request, month, year):
        salary_employees_ids = OrderEmployee.objects.values("employee_id").distinct()
        employees_salaries = []
        for employee in salary_employees_ids:
            emp = Employee.objects.get(id=employee['employee_id'])
            employee_salaries = []
            for salary in OrderEmployee.objects.filter(employee_id=emp, order_id__start_time__month=month, order_id__start_time__year=year):
                employee_salaries.append(salary)
            employees_salaries.append({'employee_id': emp.id ,'employee': emp.first_name + " " +emp.last_name, 'salaries': OrderShortEmployeeSalariesSerializer(employee_salaries, many=True).data})
        return Response(employees_salaries)


@swagger_auto_schema(method='post', request_body=OrderEmployeeSalariesChangePaidToTrueStatusSerializer)
@api_view(['POST'])
def change_paid_status(request):
    salary_ids = request.data.get('employee_salary_ids', [])
    for i in salary_ids:
        salary = OrderEmployee.objects.get(pk=i)
        salary.is_paid = True
        salary.save()
    return Response({'status': 'success', 'message': 'The salary statuses changed to paid'})
