from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from api.models import *
from api.serializers import *
from api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import requests
from rest_framework.decorators import authentication_classes, permission_classes
import uuid


def TestView(request):
    return request.data

#@authentication_classes([])
#@permission_classes([])
#@api_view(['POST','GET'])
#def LoginView(request):


class OnLogin(APIView):

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        secret = 'e90efc114a06215f1c9ddac8dcf70d4e'
        appid = 'wx77d45362c6c2763e'
        baseUrl = 'https://api.weixin.qq.com/sns/jscode2session?appid='
        extUrl1 = '&secret='
        extUrl2 = '&js_code='
        extUrl3 = '&grant_type=authorization_code'
        if request.method == 'POST':
             code = request.data.get('code')
             # nickName = request.data.get('userNickname')
             # avataUrl = request.data.get('userAvatarUrl')
             # gender = request.data.get('userGender')
             # city = request.data.get('userCity')
             # province = request.data.get('userProvince')
             # country = request.data.get('userCountry')
             # language = request.data.get('userLanguage')
             content = baseUrl + appid + extUrl1 + secret + extUrl2 + code + extUrl3
             r = requests.get(content).json()
             # validation check
             if r.get('errcode') is not None:
                 return Response(r, status=status.HTTP_400_BAD_REQUEST)
             else:
                 openid = r.get('openid')
                 session_key = r.get('session_key')
                 # do search in the database
                 userinfo = Customer.objects.filter(openid=openid)
                 if userinfo is None:
                     # add new user
                     userUuid = uuid.uuid1()
                     newuser = Customer.objects.create(openid=openid,nickName=nickName,avataUrl=avataUrl,gender=gender,city=city,province=province,country=country,language=language,uuid=userUuid)
                     newuser.save()

                     # search again to get userid
                     userinfo = Customer.objects.get(openid=openid)
                     if userinfo is not None:
                        return Response(openid)



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