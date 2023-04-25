from django.db import models
from django.utils import timezone
from objects import models as object_models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from employees import models as employee_models


class CleaningOrderType(ChoiceEnum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    COMPLAINT = 'complaint'
    OTHER = 'other'


class CleaningOrderStatus(ChoiceEnum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CONFIRMED = 'confirmed'
    OVERDUE = 'overdue'
    DECLINED = 'declined'
    OTHER = 'other'


class Order(models.Model):
    object_id = models.ForeignKey(object_models.Object, on_delete=models.CASCADE)
    type = EnumChoiceField(CleaningOrderType, default=CleaningOrderType.OTHER)
    status = EnumChoiceField(CleaningOrderStatus, default=CleaningOrderStatus.PLANNED)
    additional_information = models.TextField(blank=True, null=True)

    supervisor_comments = models.TextField(blank=True, null=True)

    report_deadline = models.DateTimeField(blank=True, null=True)
    expiration_deadline = models.DateTimeField(blank=True, null=True)
    confirmed_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    completed_time = models.DateTimeField(null=True)

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
    def order_attachments_ids(self):
        return list(self.orderattachment_set.all().values_list('id', flat=True))

    def order_attachment_evidences_ids(self):
        return list(self.orderattachmentevidence_set.values_list('id', flat=True))


class OrderAttachmentEvidence(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    attachment = models.ImageField(upload_to='documents/orders/order_attachments', null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=True, deleted_by=None):
        self.deleted = True
        self.deleted_date = timezone.now()
        # self.deleted_by = deleted_by
        self.save()


class OrderAttachment(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    attachment = models.ImageField(upload_to='documents/orders/order_attachments', null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=True, deleted_by=None):
        self.deleted = True
        self.deleted_date = timezone.now()
        # self.deleted_by = deleted_by
        self.save()


class OrderEmployee(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(employee_models.Employee, on_delete=models.SET_NULL, null=True)
    worked_hours_amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)
    def delete(self, using=None, keep_parents=True, deleted_by=None):
        self.deleted = True
        self.deleted_date = timezone.now()
        # self.deleted_by = deleted_by
        self.save()

    def payout_per_order(self):
        return self.worked_hours_amount * self.employee_id.salary

    def object_name(self):
        return self.order_id.object_id.name

    def dateOfMonth(self):
        return self.order_id.completed_time

    def employee_base_rate(self):
        return self.employee_id.salary
