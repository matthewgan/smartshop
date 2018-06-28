# Stdlib imports
# Core Django imports
from django.db import models
# Third-party app imports
# Imports from your apps
from customers.models import Customer
from shops.models import Shop


class EntranceLog(models.Model):
    who = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    where = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} visit {} @ {}".format(self.who, self.where, self.when)
