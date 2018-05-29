# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps
from merchandises.models import Merchandise


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    EPC = models.CharField(max_length=20)
    TID = models.CharField(max_length=20, blank=True)
    status = models.IntegerField(default=0)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.EPC
