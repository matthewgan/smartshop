# Stdlib imports
import uuid

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from customers.models import Customer


def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)


class UploadedFace(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=20, blank=True)
    image = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename)
    filename = models.CharField(max_length=100, blank=True)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}.{}".format(self.uuid, self.image.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.filename = self.image.name
        super(UploadedFace, self).save(force_update=force_update)
