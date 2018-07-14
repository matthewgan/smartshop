# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
import hashlib
# Imports from your apps


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    syssn = models.CharField(max_length=128, blank=True)
    out_trade_no = models.CharField(max_length=128)
    pay_type = models.CharField(max_length=128, blank=True)
    trade_status = models.CharField(max_length=32, blank=True)
    txdtm = models.DateTimeField(auto_now_add=True)
    txcurrcd = models.CharField(max_length=11)

    def __str__(self):
        return self.out_trade_no

