# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
