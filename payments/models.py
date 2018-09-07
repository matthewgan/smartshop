# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps
from customers.models import Customer


class Payment(models.Model):
    """支付统一接口记录"""
    order_method = models.IntegerField(default=0)
    user_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    trade_no = models.CharField(max_length=128)
    status = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    alipay_code_url = models.CharField(max_length=256, blank=True)
    wechat_pay_code_url = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = "统一支付记录"
        verbose_name_plural = "统一支付记录"
