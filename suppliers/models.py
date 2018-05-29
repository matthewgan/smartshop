# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from categories.models import Category


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=30)
    contactName = models.CharField(max_length=20)
    contactPhone = models.DecimalField(max_digits=11, decimal_places=0)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    ability = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    area = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.companyName

    class Meta:
        ordering = ('companyName',)
