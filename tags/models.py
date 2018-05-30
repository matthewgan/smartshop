# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps
from merchandises.models import Merchandise


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    EPC = models.CharField(max_length=24, unique=True)
    TID = models.CharField(max_length=4, blank=True)
    status = models.IntegerField(default=0)
    # status 0:stock  1:lock for pay  2:sold
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.EPC
