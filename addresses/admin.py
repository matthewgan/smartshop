from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telephone', 'detail')
    search_fields = ('name', 'detail', 'telephone',)

# Register your models here.
admin.site.register(Address, AddressAdmin)
