# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from merchandises.models import Merchandise
from shops.models import Shop


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandiseID = models.OneToOneField(Merchandise, on_delete=models.DO_NOTHING)
    clubPriceLevel1 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    clubPriceLevel2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    clubPriceLevel3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    clubPriceLevel4 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    start_time = models.DateField()
    end_time = models.DateField()
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('createTime',)
        verbose_name = "促销活动"
        verbose_name_plural = "促销活动"

