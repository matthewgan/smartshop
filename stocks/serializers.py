from rest_framework import serializers
from .models import Stock, InStockRecord, OutStockRecord


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("shopID", "merchandiseID", "number", "supplierID", )


class QueryStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("shopID", "merchandiseID")


class ListStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"
        read_only_fields = ("id", "created", "lastTime")


class InStockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InStockRecord
        fields = ("shopID", "merchandiseID", "number", "supplierID", )


class OutStockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutStockRecord
        fields = ("shopID", "merchandiseID", "number", )
