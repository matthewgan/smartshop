from django.contrib import admin
from .models import Merchandise


class MerchandiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'barcode', 'originPrice')
    search_fields = ('name', 'barcode')


admin.site.register(Merchandise, MerchandiseAdmin)
