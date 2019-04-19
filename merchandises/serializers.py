# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import Merchandise
#from  tags.models import Tag
# from inventory.models import Inventory


class MerchandiseListShowInfoSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField('render_picture_url')

    def render_picture_url(self, obj):
        fullurl = 'https://www.wuzhanggui.shop/media/merchandise_pic/' + obj.barcode + '.jpg'
        return fullurl

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace',
                  'originPrice', 'promotionPrice', 'clubPrice', 'code', 'picture', 'flavor')


# class MerchandiseListShowInfoForInventorySerializer(serializers.ModelSerializer):
#     stock = serializers.SerializerMethodField('get_inventory')
#     stockWithTag = serializers.SerializerMethodField('get_tagStock')
#
#     def get_inventory(self, obj):
#         try:
#             inventory = Inventory.objects.get(merchandiseID=obj)
#             result = inventory.stock
#         except:
#             result = '没有录入商品库存'
#         return result
#
#     def get_tagStock(self, obj):
#         try:
#             inventory = Inventory.objects.get(merchandiseID=obj)
#             result = inventory.stockWithTag
#         except:
#             result = '没有录入商品库存'
#         return result
#
#     class Meta:
#         model = Merchandise
#         fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace', 'instockPrice',
#                   'originPrice', 'promotionPrice', 'clubPrice', 'code', 'flavor', 'stock','barcode', 'stockWithTag')


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
        fields = ('code', 'barcode', 'name', 'brand', 'scale', 'factory', 'unit', 'categoryID')


class QueryMerchandiseDetailByBarcodeForCashierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace', 'originPrice', 'promotionPrice', 'clubPrice', 'code', )
