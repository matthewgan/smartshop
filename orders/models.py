# Stdlib imports

# Core Django imports
from django.db import models
from django.utils import timezone

# Third-party app imports

# Imports from your apps
from shops.models import Shop
from customers.models import Customer
from addresses.models import Address
from merchandises.models import Merchandise


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    userID = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    status = models.IntegerField(default=0)
    # status 0:waitForPay 1:waitForRecieve 2:Complete 4:Cancel 3:OfflineComplete 5:offlineWaitForPay 6:OfflineCancel
    paymentMethod = models.CharField(max_length=10)
    paymentSN = models.CharField(max_length=128, blank=True)
    tradeNo = models.CharField(max_length=128, blank=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # price before balance
    balanceUse = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # balance use by user
    payPrice = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # final pay price
    name = models.CharField(max_length=30, blank=True)  # first product name
    totalNum = models.IntegerField(default=1)
    comment = models.CharField(max_length=200, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    payTime = models.DateTimeField(default=timezone.now)
    dispatchTime = models.DateTimeField(default=timezone.now)
    receivedTime = models.DateTimeField(default=timezone.now)
    cancelTime = models.DateTimeField(default=timezone.now)
    addressID = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True)
    # addressID = models.IntegerField(blank=True)

    def __str__(self):
        return self.tradeNo

    class Meta:
        ordering = ('createTime',)


# Order details for customer order
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    orderID = models.ForeignKey(Order, related_name='details', on_delete=models.DO_NOTHING)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    merchandiseNum = models.IntegerField(default=1)
    priceOnSold = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)
