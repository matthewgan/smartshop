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


class MerchandiseListShowInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Merchandise
        fields = ('name', 'brand', 'scale', 'unit', 'producePlace', 'originPrice', 'promotionPrice', 'clubPrice')


class ShopListShowInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Shop
        fields = ('name', 'city', 'openingTime')
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


class UploadedFaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFace
        fields = ('uuid', 'image')


class BaiduUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFace
        fields = ('uuid', 'image')

