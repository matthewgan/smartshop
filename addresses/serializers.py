# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import Address


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('who',)


class AddAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
