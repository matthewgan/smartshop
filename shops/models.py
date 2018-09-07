# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    longitude = models.CharField(max_length=10, blank=True)
    latitude = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=15)
    locationDetail = models.CharField(max_length=200, blank=True)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    capacity = models.IntegerField(blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    openingTime = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('createTime',)
        verbose_name = "店铺信息"
        verbose_name_plural = "店铺信息"
