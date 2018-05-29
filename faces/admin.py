from django.contrib import admin
from .models import Face, UploadedFace

# Register your models here.
admin.site.register(Face)
admin.site.register(UploadedFace)
