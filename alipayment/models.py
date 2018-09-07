# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    trade_no = models.CharField(max_length=128, blank=True)
    out_trade_no = models.CharField(max_length=128)
    buyer_logon_id = models.CharField(max_length=128, blank=True)
    trade_status = models.CharField(max_length=32, blank=True)
    total_amount = models.CharField(max_length=11)
    invoice_amount = models.CharField(max_length=11, blank=True)
    receipt_amount = models.CharField(max_length=11, blank=True)
    store_id = models.CharField(max_length=32, blank=True)
    buyer_user_id = models.CharField(max_length=16, blank=True)
    operation = models.CharField(max_length=20)
    qr_code = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.out_trade_no

    class Meta:
        verbose_name = "支付宝支付记录"
        verbose_name_plural = "支付宝支付记录"
