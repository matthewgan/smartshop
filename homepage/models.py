from django.db import models


# Create your models here.
class Stuff(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=100, blank=True)
    image = models.CharField(max_length=200)
    title = models.CharField(max_length=40)
    profile = models.CharField(max_length=200)
    wechat = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
