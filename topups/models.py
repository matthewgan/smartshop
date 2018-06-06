# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from customers.models import Customer


class TopUp(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(default=0)
    # 0: fail 1: success
    userID = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    paymentSN = models.CharField(max_length=128, blank=True)
    tradeNo = models.CharField(max_length=128, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    amountPay = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    amountAdd = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return self.tradeNo

