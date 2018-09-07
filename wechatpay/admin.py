from django.contrib import admin
from .models import Record


class RecordAdmin(admin.ModelAdmin):
    list_display = ('out_trade_no', 'total_fee', 'timestamp', 'query_sign')


# Register your models here.
admin.site.register(Record, RecordAdmin)
