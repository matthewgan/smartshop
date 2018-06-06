# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import TopUp, TopUpGift


class CreateTopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUp
        fields = ('userID', 'amountPay', 'amountAdd',)


class TopUpSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUp
        fields = ('userID', 'tradeNo',)


class TopUpGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUpGift
        exclude = ('id', 'timestamp',)
