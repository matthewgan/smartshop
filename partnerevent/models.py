# -*- coding: utf-8 -*-
# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from partner.models import Partner


class PartnerEvent(models.Model):
    id = models.AutoField(primary_key=True)
    partner_id = models.ForeignKey(Partner, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128)
    status = models.IntegerField(default=1) # 0无效 1有效
    type = models.IntegerField(default=1)  # 类别 1.合作商户促销券(手动核销) 2.自营平台抵扣券（手/自核销）
    start_time = models.DateField()
    end_time = models.DateField()
    voucher_valid_time = models.IntegerField(default=7)  # 单位：天 优惠券有效期
    available_num = models.CharField(max_length=10)  # 总发券数量
    customer_level = models.IntegerField(default=0)  # 领取用户等级要求
    order_min = models.DecimalField(max_digits=8, decimal_places=2, default=0) # 使用条件 -类别2属性
    discount_num = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 折扣数额 -类别2属性
    discount_pre = models.DecimalField(max_digits=8, decimal_places=2, default=1)  # 折扣比例0-1 -类别2属性
    payment_min = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 获取条件
    limit = models.IntegerField(default=1)  # 每个用户领取上限
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商户促销活动"
        verbose_name_plural = "商户促销活动"
