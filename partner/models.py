# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10) # 8位 前四位区号，后四位序号
    name = models.CharField(max_length=20)
    area = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=15)
    category = models.CharField(max_length=20)
    contact_name = models.CharField(max_length=20)
    contact_tel = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "合作商户"
        verbose_name_plural = "合作商户"
