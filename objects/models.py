from django.db import models
from django.utils import timezone
from customers import models as customer_models
from employees.models import Employee


class Object(models.Model):
    customer_id = models.ForeignKey(customer_models.Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    area = models.FloatField()
    object_image_url = models.URLField(blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    required_worker_amount = models.IntegerField()
    assigned_supervisor_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    # deleted_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )

    def delete(self, using=None, keep_parents=True, deleted_by=None):
        self.deleted = True
        self.deleted_date = timezone.now()
        # self.deleted_by = deleted_by
        self.save()

    def __str__(self):
        return self.name