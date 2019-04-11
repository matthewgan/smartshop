# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'city', 'openingTime')


class CreateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'city', 'locationDetail', 'size', )
