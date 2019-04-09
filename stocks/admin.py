from django.contrib import admin
from .models import Stock, InStockRecord, OutStockRecord


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number')
    search_fields = ('merchandiseID', )


class InStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number', 'supplierID')
    search_fields = ('merchandiseID', )


class OutStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number')
    search_fields = ('merchandiseID', )


admin.site.register(Stock, StockAdmin)
admin.site.register(InStockRecord, InStockAdmin)
admin.site.register(OutStockRecord, OutStockAdmin)
