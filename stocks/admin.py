from django.contrib import admin
from .models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number', 'supplierID')
    search_fields = ('merchandiseID', )


admin.site.register(Stock, StockAdmin)
