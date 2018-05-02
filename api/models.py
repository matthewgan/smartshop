from django.db import models
from annoying.fields import AutoOneToOneField

# imports for the auth token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import requests
from django_mysql.models import ListCharField
import uuid


# create extra token when create new user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    every time a new user is saved in your database,
    this function will run and a new Token will be created for that user
    """
    if created:
        Token.objects.create(user=instance)


# Model design for wuzhanggui.shop
# Wuzhanggui User Model
class WUser(models.Model):
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    # user identify from Wechat
    openid = models.CharField(max_length=30, blank=True)
    session_key = models.CharField(max_length=30, blank=True)
    code = models.CharField(max_length=32, default=None)
    # Get UserInfo from wechat login
    nickName = models.CharField(max_length=32)
    avatarUrl = models.URLField(max_length=200, blank=True)
    gender = models.IntegerField(default=2)
    city = models.CharField(max_length=15, blank=True)
    province = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=15, blank=True)
    language = models.CharField(max_length=15, blank=True)
    # Self defined user info
    level = models.IntegerField(default=1)
    point = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    faceExisted = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        super(WUser, self).save(*args, **kwargs)

    class Meta:
        ordering = ('createTime',)


# Customer Face Model
class Face(models.Model):
    who = models.ForeignKey(WUser, on_delete=models.CASCADE)
    # identify ids from baidu
    baidu_appid = models.CharField(max_length=128)
    baidu_group_id = models.CharField(max_length=128)
    baidu_uid = models.CharField(max_length=128)
    baidu_faceid = models.CharField(max_length=128)

    def __str__(self):
        return self.who


# Customer Delivery Address Model
class Address(models.Model):
    who = models.ForeignKey(WUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    telephone = models.DecimalField(max_digits=11, decimal_places=0)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    detail = models.CharField(max_length=50)
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return self.detail[:10]


# Merchandise Category Model
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Merchandise Information Model
class Merchandise(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    barcode = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=30, blank=True)
    brand = models.CharField(max_length=10, blank=True)
    originPrice = models.DecimalField(max_digits=8, decimal_places=2)
    scale = models.CharField(max_length=10, blank=True)
    factory = models.CharField(max_length=30, blank=True)
    priceChecker = models.CharField(max_length=10, blank=True)
    supervisionCode = models.CharField(max_length=30, blank=True)
    supervisor = models.CharField(max_length=20, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    supervisorTel = models.DecimalField(max_digits=11, decimal_places=0, blank=True)
    promotionPrice = models.DecimalField(max_digits=8, decimal_places=2, default=originPrice)
    clubPrice = models.DecimalField(max_digits=8, decimal_places=2, default=originPrice)
    producePlace = models.CharField(max_length=10, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('createTime',)


# Shop Model
class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    longitude = models.CharField(max_length=10, blank=True)
    latitude = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=15)
    locationDetail = models.CharField(max_length=200, blank=True)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    capacity = models.IntegerField(blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    openingTime = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('createTime',)


# Sale Event Model
class SaleEvent(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey('Shop', on_delete=models.DO_NOTHING)
    merchandiseID = models.OneToOneField(Merchandise, on_delete=models.DO_NOTHING)
    clubPriceLevel1 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    clubPriceLevel2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    clubPriceLevel3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    clubPriceLevel4 = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    start_time = models.DateField()
    end_time = models.DateField()
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('createTime',)


# Rack Model
class Rack(models.Model):
    id = models.AutoField(primary_key=True)
    length = models.IntegerField(default=900)
    width = models.IntegerField(default=320)
    height = models.IntegerField(default=1600)
    level = models.IntegerField(default=4)
    capacity = models.IntegerField(blank=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Shop%s:%s" % (self.shopID, self.id)


# Merchandise Supplier Model
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=30)
    contactName = models.CharField(max_length=20)
    contactPhone = models.DecimalField(max_digits=11, decimal_places=0)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    ability = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    area = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.companyName

    class Meta:
        ordering = ('companyName',)


# Stock Model for shops
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    number = models.IntegerField(default=1)
    arriveDate = models.DateField()
    supplierID = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('createTime',)


# Order Model for customers
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    userID = models.ForeignKey(WUser, on_delete=models.DO_NOTHING)
    status = models.IntegerField(default=3)
    paymentMethod = models.CharField(max_length=10)
    paymentSN = models.CharField(max_length=30)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    delivery = models.DecimalField(max_digits=8, decimal_places=2)
    bill = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.CharField(max_length=200, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    payTime = models.DateTimeField(blank=True)
    dispatchTime = models.DateTimeField(blank=True)
    receivedTime = models.DateTimeField(blank=True)
    cancelTime = models.DateTimeField(blank=True)
    addressID = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('createTime',)


# Order details for customer order
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)
    merchandiseNum = models.IntegerField(default=1)

    def __str__(self):
        return self.id


# ESL electronic shelves label Model
class ESL(models.Model):
    id = models.AutoField(primary_key=True)
    labelID = models.CharField(max_length=8)
    merchandiseID = models.OneToOneField(Merchandise, on_delete=models.DO_NOTHING)
    rackID = models.ForeignKey(Rack, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.labelID


class RFIDtag(models.Model):
    id = models.AutoField(primary_key=True)
    EPC = models.CharField(max_length=20)
    TID = models.CharField(max_length=20, blank=True)
    status = models.IntegerField(default=0)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.EPC