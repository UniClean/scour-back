from django.db import models
from django.utils import timezone
from objects import models as object_models


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    amount = models.IntegerField(default=1)
    # на каком объекте находится оборудование
    object_id = models.ForeignKey(object_models.Object, on_delete=models.CASCADE, blank=True, null=True)

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