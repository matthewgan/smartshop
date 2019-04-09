from rest_framework import serializers
from .models import SaleRecord


class SaleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleRecord
        fields = "__all__"
