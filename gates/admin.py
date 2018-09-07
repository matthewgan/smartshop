from django.contrib import admin
from .models import EntranceLog


class EntranceLogAdmin(admin.ModelAdmin):
    list_display = ('who', 'where', 'when')
    search_fields = ('who', 'when')


admin.site.register(EntranceLog, EntranceLogAdmin)
