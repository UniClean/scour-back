from django.db import models
from django.utils import timezone
import os

class Customer(models.Model):
    name = models.CharField(max_length=100)
    is_vip = models.BooleanField(default=False)
    additional_information = models.TextField(blank=True, null=True)

    email = models.CharField(max_length=150, null=True)
    website = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=150, null=True)

    image_url = models.URLField(blank=True, null=True)
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

    def customer_contract_ids(self):
        return list(self.customercontract_set.values_list('id', flat=True))


class CustomerContract(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    contract_file = models.FileField(upload_to='documents/customers/customer_contract_files', null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=True):

        self.deleted = True
        self.deleted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.contract_url

class CustomerImage(models.Model):
    image = models.ImageField(upload_to='customer_images')

    def __str__(self):
        return self.image_url
