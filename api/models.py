from django.db import models
from annoying.fields import AutoOneToOneField

# imports for the auth token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    every time a new user is saved in your database,
    this function will run and a new Token will be created for that user
    """
    if created:
        Token.objects.create(user=instance)


GENDER_DEFINES = (
            ('1', 'Male'),
            ('2', 'Female'),
            ('0', 'Unknown'),
        )


# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=30, blank=True)
    openid = models.CharField(max_length=32, blank=True)
    session_key = models.CharField(max_length=32, blank=True)
    nickName = models.CharField(max_length=32, blank=True)
    avatarUrl = models.URLField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_DEFINES)
    city = models.CharField(max_length=15, blank=True)
    province = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=15, blank=True)
    language = models.CharField(max_length=15, blank=True)
    level = models.CharField(max_length=15, blank=True)
    point = models.CharField(max_length=15, blank=True)
    faceId = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='customers', on_delete=models.CASCADE)

    def __str__(self):
        return self.nickName

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)


class WxUser(models.Model):
    userid = AutoOneToOneField(Customer, primary_key=True)
    code = models.CharField(max_length=32)
    openid = models.CharField(max_length=32)
    session_key = models.CharField(max_length=32)
    unionid = models.CharField(max_length=32, blank=True)
    third_session = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.openid

    class Meta:
        ordering = ('created',)


class Face(models.Model):
    userid = AutoOneToOneField(Customer, primary_key=True)
    image = models.ImageField(upload_to='face_images')


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey('auth.User', related_name='shops', on_delete=models.CASCADE)
    rack_capacity = models.IntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    opening = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)


class Rack(models.Model):
    rackID = models.AutoField(primary_key=True)
    length = models.IntegerField(default=900)
    width = models.IntegerField(default=320)
    height = models.IntegerField(default=1600)
    level = models.IntegerField(default=4)
    product_capacity = models.IntegerField(blank=True)


class Category(models.Model):
    catID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    supplierID = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=30)
    contactName = models.CharField(max_length=20)
    contactPhone = models.DecimalField(max_digits=20, decimal_places=0)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.companyName


class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unitPrice = models.DecimalField(max_digits=5, decimal_places=2)
    unitInStock = models.IntegerField()
    unitOnOrder = models.IntegerField()
    QuantityPerUnit = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    userID = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    productID = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    payMethod = models.CharField(max_length=20)
    timeStamp = models.DateTimeField(auto_now_add=True)


class ESL(models.Model):
    etagID = models.AutoField(primary_key=True)
    modulePin = models.CharField(max_length=20, unique=True)
    rackID = models.ForeignKey(Rack, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.modulePin


class RFID(models.Model):
    rtagID = models.AutoField(primary_key=True)
    PIN = models.CharField(max_length=30, unique=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=None)

    def __str__(self):
        return self.PIN
