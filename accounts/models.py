from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from employees.models import Employee


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    def delete(self, using=None, keep_parents=True, deleted_by=None):
        self.deleted = True
        self.deleted_date = timezone.now()
        # self.deleted_by = deleted_by
        self.save()

