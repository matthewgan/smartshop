# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from partner.models import Partner


class PartnerEvent(models.Model):
    id = models.AutoField(primary_key=True)
    partner_id = models.ForeignKey(Partner, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20)
    status = models.IntegerField(default=1)
    start_time = models.DateField()
    end_time = models.DateField()
    voucher_valid_time = models.IntegerField(default=7)  # 单位：天 优惠券有效期
    available_num = models.CharField(max_length=10)
    customer_level = models.IntegerField(default=0)
    payment_min = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    limit = models.IntegerField(default=1)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.name
