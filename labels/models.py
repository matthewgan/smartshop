# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from merchandises.models import Merchandise
from racks.models import Rack


class Label(models.Model):
    id = models.AutoField(primary_key=True)
    labelID = models.CharField(max_length=8)
    merchandiseID = models.OneToOneField(Merchandise, on_delete=models.DO_NOTHING)
    rackID = models.ForeignKey(Rack, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.labelID

    class Meta:
        verbose_name = "墨水屏价格标签"
        verbose_name_plural = "墨水屏价格标签"
