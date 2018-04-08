from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Customer
        exclude = ('created', )


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    customers = serializers.PrimaryKeyRelatedField(many=True, queryset=Customer.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'customers',)


class WxUserSerializer(serializers.HyperlinkedModelSerializer):
    userid = serializers.HyperlinkedIdentityField(view_name="api:wxuser-detail")

    class Meta:
        model = WxUser
        fields = ('userid', 'code', 'openid', 'created',)


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class RackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rack
        fields = '__all__'


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ESLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ESL
        fields = '__all__'


class RFIDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RFID
        fields = '__all__'
