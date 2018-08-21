# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    # User identify from Wechat
    openid = models.CharField(max_length=30, blank=True)
    session_key = models.CharField(max_length=30, blank=True)
    code = models.CharField(max_length=32, default=None)
    # Get UserInfo from wechat login
    nickName = models.CharField(max_length=32)
    avatarUrl = models.URLField(max_length=200, blank=True)
    gender = models.IntegerField(default=2)
    city = models.CharField(max_length=30, blank=True)
    province = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=30, blank=True)
    # Self defined user info
    level = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    faceExisted = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.id, self.nickName)

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        ordering = ('createTime',)
