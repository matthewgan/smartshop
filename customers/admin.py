from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'nickName', 'gender', 'level', 'point', 'balance', 'createTime', 'updateTime')
    search_fields = ('id', 'nickName',)


admin.site.register(Customer, CustomerAdmin)
