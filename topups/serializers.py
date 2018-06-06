# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import TopUp


class CreateTopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUp
        fields = ('userID', 'amountPay', 'amountAdd')
