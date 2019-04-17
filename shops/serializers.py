# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
        read_only_fields = ('id', 'createTime', )


class CreateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'city', 'locationDetail', 'size', )
