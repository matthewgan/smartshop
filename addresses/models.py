# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from customers.models import Customer


class Address(models.Model):
    who = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    telephone = models.DecimalField(max_digits=11, decimal_places=0)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    detail = models.CharField(max_length=50)
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return self.detail[:10]
