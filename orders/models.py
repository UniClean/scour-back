from django.db import models
from django.utils import timezone
from objects import models as object_models

import enum


class CleaningOrderType(enum.Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    COMPLAINT = 'complaint'
    OTHER = 'other'


class CleaningOrderStatus(enum.Enum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CONFIRMED = 'confirmed'
    OVERDUE = 'overdue'
    DECLINED = 'declined'
    OTHER = 'other'


class Order(models.Model):
    object_id = models.ForeignKey(object_models.Object, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=[(tag.name, tag.value) for tag in CleaningOrderType])
    status = models.CharField(max_length=100, choices=[(tag.name, tag.value) for tag in CleaningOrderStatus],
                              default=CleaningOrderStatus.PLANNED.name)
    additional_information = models.TextField(blank=True, null=True)
    accept_time = models.DateTimeField(null=True)
    completed_time = models.DateTimeField(null=True)
    supervisor_comments = models.TextField(blank=True, null=True)

    report_deadline = models.DateTimeField(blank=True, null=True)
    start_when = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=True, deleted_by=None):
        self.deleted = True
        self.deleted_date = timezone.now()
        # self.deleted_by = deleted_by
        self.save()



    # deleted_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )
# Create your models here.
