from django.contrib import admin
from .models import Position, Employee, EmployeeDocument

# Register your models here.
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(EmployeeDocument)
