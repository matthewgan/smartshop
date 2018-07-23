# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps
from categories.models import Category


class Merchandise(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=15)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=30, blank=True)
    flavor = models.CharField(max_length=30, blank=True)
    scale = models.CharField(max_length=10, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    factory = models.CharField(max_length=30, blank=True)
    producePlace = models.CharField(max_length=10, blank=True)
    purchasePrice = models.DecimalField(max_digits=8, decimal_places=2)
    originPrice = models.DecimalField(max_digits=8, decimal_places=2)
    promotionPrice = models.DecimalField(max_digits=8, decimal_places=2, default=originPrice)
    clubPrice = models.DecimalField(max_digits=8, decimal_places=2, default=originPrice)
    priceChecker = models.CharField(max_length=10, blank=True)
    supervisionCode = models.CharField(max_length=30, blank=True)
    supervisor = models.CharField(max_length=20, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    # picture = models.ImageField("Uploaded image/MerchandiseImg", upload_to=scramble_uploaded_filename)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('createTime',)
