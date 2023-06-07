from django.db import models
from django.utils import timezone
from enumchoicefield import ChoiceEnum, EnumChoiceField

class Rate(ChoiceEnum):
    HOUR = 'hour'
    MONTH = 'month'
    OTHER = 'other'

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position_id = models.ForeignKey('Position', on_delete=models.SET_NULL , blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()
    date_of_employment = models.DateTimeField()
    salary = models.FloatField()
    rate = EnumChoiceField(Rate, default=Rate.HOUR)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)


    def delete(self, using=None, keep_parents=True):
        self.deleted = True
        self.deleted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['created']


class EmployeeDocument(models.Model):
    document_url = models.URLField()
    employee_id = models.ForeignKey('Employee', on_delete=models.SET_NULL , blank=True, null=True)


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

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