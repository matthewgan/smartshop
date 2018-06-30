from django.db import models
from customers.models import Customer


# Create your models here.
class FaceRecord(models.Model):
    id = models.AutoField(primary_key=True);
    token = models.CharField(max_length=100, blank=True)
    score = models.FloatField(default=0.0)
    user_id = models.CharField(max_length=20)
    user_info = models.CharField(max_length=100, blank=True)
    group_id = models.CharField(max_length=20, default="customer")
    operation = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}.{}".format(self.user_id, self.operation)
