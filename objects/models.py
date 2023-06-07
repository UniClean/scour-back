from django.db import models
from django.utils import timezone
from customers import models as customer_models
from employees.models import Employee
from inventory import models as inventory_models


class Object(models.Model):
    customer_id = models.ForeignKey(customer_models.Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    area = models.FloatField()
    object_image = models.ImageField(upload_to='images/objects/', blank=True, null=True)
    object_image_url = models.URLField(blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    required_worker_amount = models.IntegerField()
    assigned_supervisor_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)


    def delete(self, using=None, keep_parents=True):
        self.deleted = True
        self.deleted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class RequiredObjectInventory(models.Model):
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE)
    inventory_id = models.ForeignKey(inventory_models.Inventory, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=True):
        self.deleted = True
        self.deleted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

