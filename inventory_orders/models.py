from django.db import models
from objects.models import RequiredObjectInventory, Object
from django.utils import timezone
from enumchoicefield import ChoiceEnum, EnumChoiceField


class InventoryOrderStatus(ChoiceEnum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    DECLINED = 'declined'
    OTHER = 'other'


class InventoryOrder(models.Model):
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE, null=True)
    deadline = models.DateTimeField()
    status = EnumChoiceField(InventoryOrderStatus, default=InventoryOrderStatus.CREATED)

    in_progress_time = models.DateTimeField(null=True)
    completed_time = models.DateTimeField(null=True)

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


class InventoryOrderItem(models.Model):
    inventory_order_id = models.ForeignKey(InventoryOrder, on_delete=models.SET_NULL, blank=True, null=True)
    required_object_inventory_id = models.ForeignKey(RequiredObjectInventory, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()

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