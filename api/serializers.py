from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User


class WUserLoginRequestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WUser
        fields = ('code', 'nickName', 'avatarUrl', 'city', 'province', 'country', 'gender', 'language')


class WUserLoginResponseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WUser
        fields = ('id', 'point', 'level', 'balance', 'faceExisted')


class WUserSetCodeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = WUser
        fields = ('id', 'code')


class WUserSetCodeResponseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WUser
        fields = ('id', 'point', 'level', 'balance')


class WUserListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WUser
        fields = '__all__'


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class MerchandiseListAllInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Merchandise
        fields = '__all__'


class ShopListShowInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Shop
        fields = ('name', 'city', 'openingTime')


class CategoryResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class MerchandiseListShowInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace', 'originPrice', 'promotionPrice', 'clubPrice')


class OrderListShowSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = fields = ('id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery',
                           'totalPrice', 'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'createTime', 'cancelTime', )


class OrderListProductInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchandise
        fields = ('name', 'promotionPrice', )


class OrderDetailSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='merchandiseID.name', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ('merchandiseID', 'merchandiseNum', 'priceOnbill', 'name')


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
            OrderDetail.objects.create(order=order, **details_data)
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
            OrderDetail.objects.create(order=order, **details_data)
        return order


class CreateTopUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('userID', 'tradeNo', 'amount')


# class OrderListResponseSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = ('shopID', 'paymentSN', 'delivery', 'totalPrice', 'balanceUse', 'payPrice', 'addressID', 'details', )


class AddressListSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('who',)


class AddAddressSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

class WeChatPayOrderSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

#
# class ShopSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Shop
#         fields = '__all__'
#
#
# class RackSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Rack
#         fields = '__all__'
#
#
# class SupplierSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Supplier
#         fields = '__all__'
#
#
# class ProductSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#
# class OrderSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#
#
#
# class ESLSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ESL
#         fields = '__all__'
#
#
# class RFIDSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = RFID
#         fields = '__all__'


class UploadedFaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFace
        fields = ('uuid', 'image')


class EntranceGetInfoRequestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WUser
        fields = 'code'


class EntranceGetInfoResponseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WUser
        fields = ('avatarUrl', 'nikeName', 'level')


class SearchFaceUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFace
        fields = 'image'

