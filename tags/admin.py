from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'EPC', 'status', 'merchandiseID', )
    search_fields = ('EPC', 'merchandiseID')


# Register your models here.
admin.site.register(Tag, TagAdmin)
