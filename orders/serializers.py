# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import Order, OrderDetail


class OrderListShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = fields = ('id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery', 'payTime',
                           'totalPrice', 'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'createTime', 'cancelTime', 'tradeNo')


class OrderDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='merchandiseID.name', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ('merchandiseID', 'merchandiseNum', 'priceOnSold', 'name')


class CreateOrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'userID', 'shopID', 'status', 'paymentMethod', 'discount', 'delivery', 'totalPrice',
                  'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'details', 'createTime','tradeNo', )

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for details_data in details_data:
            OrderDetail.objects.create(orderID=order, **details_data)
        return order


class GetOrderDetailSerializer(serializers.ModelSerializer):
    addName = serializers.CharField(source='addressID.name')
    addTel = serializers.CharField(source='addressID.telephone')
    addDetail = serializers.CharField(source='addressID.detail')
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery', 'totalPrice',
                  'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'details', 'createTime', 'addName', 'addTel', 'addDetail')

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for details_data in details_data:
            OrderDetail.objects.create(orderID=order, **details_data)
        return order


class WeChatPayOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderResponseSerializer(serializers.HyperlinkedModelSerializer):
    order_details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('userID', 'shopID', 'discount', 'bill')