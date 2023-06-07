from django.db import models
from django.utils import timezone


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()

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