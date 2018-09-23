# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import Payment
from orders.models import Order


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('order_method', 'user_id', 'trade_no')


class PaymentResponseSerializer(serializers.ModelSerializer):
    payPrice = serializers.SerializerMethodField('getPayPrice')
    balanceUse = serializers.SerializerMethodField('getBalanceUse')
    discount = serializers.SerializerMethodField('getDiscount')

    def getPayPrice(self, obj):
        order = Order.objects.get(tradeNo=obj.trade_no)
        payPrice = order.payPrice
        return payPrice

    def getBalanceUse(self, obj):
        order = Order.objects.get(tradeNo=obj.trade_no)
        balanceUse = order.balanceUse
        return balanceUse

    def getDiscount(self, obj):
        order = Order.objects.get(tradeNo=obj.trade_no)
        discount = order.discount
        return discount

    class Meta:
        model = Payment
        fields = ('status', 'balanceUse', 'discount', 'alipay_code_url', 'wechat_pay_code_url', 'payPrice')
