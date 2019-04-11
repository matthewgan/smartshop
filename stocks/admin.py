from django.contrib import admin
from .models import Stock, InStockRecord, OutStockRecord, TransferStockRecord


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number')
    search_fields = ('merchandiseID', )


class InStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number', 'supplierID', 'operator')
    search_fields = ('merchandiseID', )


class OutStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopID', 'merchandiseID', 'number', 'operator')
    search_fields = ('merchandiseID', )


class TransferStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'fromShop', 'toShop', 'merchandiseID', 'number', 'operator')
    search_fields = ('merchandiseID',)


admin.site.register(Stock, StockAdmin)
admin.site.register(InStockRecord, InStockAdmin)
admin.site.register(OutStockRecord, OutStockAdmin)
admin.site.register(TransferStockRecord, TransferStockAdmin)
