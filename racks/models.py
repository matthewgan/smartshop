# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from shops.models import Shop


class Rack(models.Model):
    id = models.AutoField(primary_key=True)
    length = models.IntegerField(default=900)
    width = models.IntegerField(default=320)
    height = models.IntegerField(default=1600)
    level = models.IntegerField(default=4)
    capacity = models.IntegerField(blank=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Shop%s:%s" % (self.shopID, self.id)

    class Meta:
        verbose_name = "货架"
        verbose_name_plural = "货架"
