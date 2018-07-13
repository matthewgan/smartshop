# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import Payment


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('order_method', 'user_id', 'trade_no')


class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('status', 'balance', 'alipay_code_url', 'wechat_pay_code_url')
