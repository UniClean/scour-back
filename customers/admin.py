from django.contrib import admin
from .models import Customer, CustomerContract, CustomerImage

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerContract)
admin.site.register(CustomerImage)