from django.contrib import admin
from .models import SaleRecord


class SaleRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'merchandise', 'number', 'created', 'updated')
    search_fields = ('merchandise', )


admin.site.register(SaleRecord, SaleRecordAdmin)
