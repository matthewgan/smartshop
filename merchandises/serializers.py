# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import Merchandise
from  tags.models import Tag


class MerchandiseListShowInfoSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField('render_picture_url')

    def render_picture_url(self, obj):
        fullurl = 'https://www.wuzhanggui.shop/media/merchandise_pic/' + obj.barcode + '.jpg'
        return fullurl

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace',
                  'originPrice', 'promotionPrice', 'clubPrice', 'code', 'picture', 'flavor')


class MerchandiseListAllInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = '__all__'


class OrderListMerchandiseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('name', 'promotionPrice', )


class QueryMerchandiseDetailByBarcodeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('barcode',)


class QueryMerchandiseDetailByBarcodeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('id', 'code', 'barcode', 'name', 'brand', 'scale', 'factory', 'unit', 'flavor')


class AddMerchandiseDetailByBarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('code', 'barcode', 'name', 'brand', 'scale', 'factory', 'unit',)


class QueryMerchandiseDetailByBarcodeForCashierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace', 'originPrice', 'promotionPrice',
                           'clubPrice', 'code', )
