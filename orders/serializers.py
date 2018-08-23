# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import Order, OrderDetail
from merchandises.models import Merchandise


class OrderListShowSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField('render_picture_url')

    def render_picture_url(self, obj):
        merchandise = Merchandise.objects.get(code=obj.code)
        fullurl = 'https://www.wuzhanggui.shop/media/merchandise_pic/' + merchandise.barcode + '.jpg'
        return fullurl

    class Meta:
        model = Order
        fields = ('id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery', 'payTime',
                           'totalPrice', 'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'createTime', 'cancelTime', 'tradeNo', 'picture')


class OrderDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='merchandiseID.name', read_only=True)
    picture = serializers.SerializerMethodField('render_picture_url')

    def render_picture_url(self, obj):
        fullurl = 'https://www.wuzhanggui.shop/media/merchandise_pic/' + obj.merchandiseID.barcode + '.jpg'
        return fullurl

    class Meta:
        model = OrderDetail
        fields = ('merchandiseID', 'merchandiseNum', 'priceOnSold', 'name', 'picture', )


class CreateOrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'userID', 'shopID', 'status', 'paymentMethod', 'discount', 'delivery', 'totalPrice',
                  'balanceUse', 'payPrice', 'name', 'code', 'totalNum', 'comment', 'addressID', 'details', 'createTime','tradeNo', )

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
                  'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'details', 'createTime',
                  'addName', 'addTel', 'addDetail', 'tradeNo',)

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for details_data in details_data:
            OrderDetail.objects.create(orderID=order, **details_data)
        return order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderResponseSerializer(serializers.HyperlinkedModelSerializer):
    order_details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('userID', 'shopID', 'discount', 'bill')


class OrderDetailForConfirmSerializer(serializers.ModelSerializer):
    merchandise_name = serializers.CharField(source='merchandiseID.name')
    merchandise_code = serializers.CharField(source='merchandiseID.code')
    merchandise_subCategoryName = serializers.CharField(source='merchandiseID.subCategoryName')

    class Meta:
        model = OrderDetail
        fields = ('merchandiseNum', 'merchandise_name', 'merchandise_code', 'merchandise_subCategoryName')


class OrderListForConfirmSerializer(serializers.ModelSerializer):
    add_name = serializers.CharField(source='addressID.name')
    add_tel = serializers.CharField(source='addressID.telephone')
    add_detail = serializers.CharField(source='addressID.detail')
    details = OrderDetailForConfirmSerializer(many=True)

    class Meta:
        model = Order
        fields = ('add_name', 'add_tel', 'add_detail', 'payTime', 'details', 'totalPrice', 'tradeNo')