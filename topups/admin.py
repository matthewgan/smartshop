from django.contrib import admin
from .models import TopUp, TopUpGift


class TopUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'tradeNo', 'paymentSN', 'amountPay', 'amountAdd', 'createTime')
    search_fields = ('userID', )


# Register your models here.
admin.site.register(TopUp, TopUpAdmin)
admin.site.register(TopUpGift)
