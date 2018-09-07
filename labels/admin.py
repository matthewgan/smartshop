from django.contrib import admin
from .models import Label


class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'labelID', 'merchandiseID', 'rackID')
    search_fields = ('labelID', )


admin.site.register(Label, LabelAdmin)
