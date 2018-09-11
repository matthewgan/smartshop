# Stdlib imports

# Core Django imports
from django.db import models
from django.utils import timezone

from merchandises.models import Merchandise


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    stockWithTag = models.IntegerField(default=0)

    def __str__(self):
        return self.merchandiseID

    class Meta:
        ordering = ('merchandiseID',)


class InventoryRecord(models.Model):
    id = models.AutoField(primary_key=True)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    instockPrice = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    retailPrice = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    productionDate = models.DateTimeField()
    expiryDate = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    createTime = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=128)

    def __str__(self):
        return self.merchandiseID

    class Meta:
        ordering = ('createTime',)