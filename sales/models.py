from django.db import models
from merchandises.models import Merchandise
from shops.models import Shop


class SaleRecord(models.Model):
    id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def record(self, sale_number):
        self.number += sale_number
        self.save()

    class Meta:
        ordering = ('updated', )
        verbose_name = "销售记录"
        verbose_name_plural = "销售记录"
