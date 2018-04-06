from django.shortcuts import render
from rest_framework import viewsets, permissions
from api.models import *
from api.serializers import *
from api.permissions import IsOwnerOrReadOnly
#from rest_framework.decorators import api_view
#from rest_framework.response import Response
from django.contrib.auth.models import User



class CustomerViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OwnerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = OwnerSerializer


class WxUserViewSet(viewsets.ModelViewSet):
    queryset = WxUser.objects.all()
    serializer_class = WxUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ESLViewSet(viewsets.ModelViewSet):
    queryset = ESL.objects.all()
    serializer_class = ESLSerializer


class RFIDViewSet(viewsets.ModelViewSet):
    queryset = RFID.objects.all()
    serializer_class = RFIDSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer