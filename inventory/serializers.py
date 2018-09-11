# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
from .models import InventoryRecord


class AddRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = InventoryRecord
        fields = ('merchandiseID', 'instockPrice', 'retailPrice', 'productionDate', 'expiryDate', 'quantity', 'supplier')