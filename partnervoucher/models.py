# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports
from django.utils import timezone

# Imports from your apps
from partnerevent.models import PartnerEvent
from customers.models import Customer


class PartnerVoucher(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)  # 前三位：合作商id 中间五位：随机数 后十位：时间戳
    event_id = models.ForeignKey(PartnerEvent, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    create_time = models.DateField(auto_now_add=True)
    end_time = models.DateField()
    use_time = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "合作促销券"
        verbose_name_plural = "合作促销券"
