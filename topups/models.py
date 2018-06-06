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


class TopUpGift(models.Model):
    id = models.AutoField(primary_key=True)
    level0topup = models.IntegerField(default=20)
    level0gift = models.IntegerField(default=0)
    level1topup = models.IntegerField(default=50)
    level1gift = models.IntegerField(default=3)
    level2topup = models.IntegerField(default=100)
    level2gift = models.IntegerField(default=8)
    level3topup = models.IntegerField(default=200)
    level3gift = models.IntegerField(default=20)
    level4topup = models.IntegerField(default=500)
    level4gift = models.IntegerField(default=60)
    level5topup = models.IntegerField(default=1000)
    level5gift = models.IntegerField(default=150)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.id, self.timestamp)
