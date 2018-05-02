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
        fields = ('uuid', 'point', 'level', 'balance', 'faceExisted')


class WUserListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = WUser
        fields = '__all__'


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    wusers = serializers.PrimaryKeyRelatedField(many=True, queryset=WUser.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'customers',)


# class WxUserSerializer(serializers.HyperlinkedModelSerializer):
#     userid = serializers.HyperlinkedIdentityField(view_name="api:wxuser-detail")
#
#     class Meta:
#         model = WxUser
#         fields = ('userid', 'code', 'openid', 'created',)
#
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
# class CategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'
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
