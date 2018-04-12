from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from api.models import *
from api.serializers import *
from api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import requests
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([])
@permission_classes([])
def TestView(request):
    return request.data


@api_view(['GET'])
def LoginView(request):
    secret = '83d851c655e5c4ba714decda83ad5c6b'
    appid = 'wx23c4e200139a74ee'
    baseUrl = 'https://api.weixin.qq.com/sns/jscode2session?appid='
    extUrl1 = '&secret='
    extUrl2 = '&js_code='
    extUrl3 = '&grant_type=authorization_code'
    if request.method == 'GET':
        code = request.data.get('code')
        content = baseUrl + appid + extUrl1 + secret + extUrl2 + str(code) + extUrl3
        r = requests.get(content).json()
        # validation check
        if r.get('errcode') is not None:
            return Response(r, status=status.HTTP_400_BAD_REQUEST)
        else:
            openid = r.get('openid')
            session_key = r.get('session_key')
            unionid = r.get('unionid')
            # do search in the database
            userinfo = WxUser.objects.filter(openid=openid)
            if userinfo is None:
                # add new user
                newuser = WxUser.objects.create(code=code, openid=openid, session_key=session_key, unionid=unionid)
                newuser.save()
                isNew = True
                # search again to get userid
                userinfo = WxUser.objects.get(openid=openid)



class CustomerViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

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
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@authentication_classes([])
@permission_classes([])
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