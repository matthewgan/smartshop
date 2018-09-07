# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from shops.models import Shop
from merchandises.models import Merchandise
from suppliers.models import Supplier


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    number = models.IntegerField(default=1)
    arriveDate = models.DateField()
    supplierID = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('createTime',)
        verbose_name = "库存记录"
        verbose_name_plural = "库存记录"
