# Stdlib imports

# Core Django imports
from django.db import models
from django.contrib.auth.models import User

# Third-party app imports

# Imports from your apps
from shops.models import Shop
from merchandises.models import Merchandise
from suppliers.models import Supplier


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=1)
    supplierID = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def instock(self, instock_number):
        self.number += instock_number
        self.save()

    def outstock(self, outstock_number):
        if (self.number - outstock_number) >= 0:
            self.number -= outstock_number
        else:
            self.number = 0
        self.save()

    class Meta:
        ordering = ('created',)
        verbose_name = "库存信息"
        verbose_name_plural = "库存信息"


class InStockRecord(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=1)
    supplierID = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('created',)
        verbose_name = "入库记录"
        verbose_name_plural = "入库记录"


class OutStockRecord(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('created',)
        verbose_name = "出库记录"
        verbose_name_plural = "出库记录"


class TransferStockRecord(models.Model):
    id = models.AutoField(primary_key=True)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=1)
    fromShop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, related_name="transfer_from_shop")
    toShop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, related_name="transfer_to_shop")
    created = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    result = models.BooleanField(default=False)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('created',)
        verbose_name = "转仓记录"
        verbose_name_plural = "转仓记录"
