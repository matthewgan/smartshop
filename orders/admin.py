from django.contrib import admin
from .models import Order, OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'tradeNo', 'userID', 'status', 'totalPrice', 'createTime', 'payTime', 'cancelTime', )
    search_fields = ('tradeNo', 'userID', 'totalPrice', 'createTime')


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderID', 'merchandiseID', 'merchandiseNum', )
    search_fields = ('orderID', 'merchandiseID')


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
