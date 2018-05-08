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
#import uuid
from django.http import JsonResponse
from django.http import Http404


class WUserCreateOrListView(APIView):
    """
    List all the wechat users, or create a new user
    """
    def get(self, request, *args, **kwargs):
        """
        List all the wechat user in the database
        Need to add permission control later
        Only show to shop owners and system admins
        """
        wusers = WUser.objects.all()
        serializer = WUserListSerializer(wusers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Receive post message from wechat mini app,
        check if user is new to create a new user,
        else search the database and reply user's and infos
        """
        serializer = WUserLoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            # Use code to Request wxid and sessionkey from wechat API
            # appid and secret from wechat miniapp website
            wxapp_secret = 'e90efc114a06215f1c9ddac8dcf70d4e'
            wxapp_appid = 'wx77d45362c6c2763e'
            # fixed wechat API address for wx.login
            baseurl = 'https://api.weixin.qq.com/sns/jscode2session?appid='
            content = baseurl + wxapp_appid + '&secret=' + wxapp_secret + '&js_code=' + code + '&grant_type=authorization_code'
            # request wechat API and get json response
            res = requests.get(content).json()
            if res.get('errcode') is not None:
                return Response(res, status=status.HTTP_204_NO_CONTENT)
            else:
                openid = res.get('openid')
                session_key = res.get('session_key')
                # do search on the database to see if the user is already existed
                try:
                    wuser = WUser.objects.get(openid=openid)
                except WUser.DoesNotExist:
                    wuser = serializer.create(serializer.validated_data)
                    wuser.openid = openid
                    wuser.session_key = session_key
                    wuser.save()
                output_serializer = WUserLoginResponseSerializer(wuser)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WXUserSetCodeView(APIView):
    """
    3.1.3 每次打开小程序上传code（uuid=ture）
    """
    def post(self, request):
        serializer = WUserSetCodeRequestSerializer(data=request.data)
        # print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            wuser = WUser.objects.get(pk=serializer.validated_data.get['id'])
            wuser.code = serializer.validated_data['code']
            #wuser.save()
            output_serializer = WUserSetCodeResponseSerializer(wuser)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(APIView):
    """
    List all the categories in the database: ids & names
    for wechat mini app
    """
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)


class MerchandisesShowByCategoryView(APIView):
    """
    List all the merchandises under specified category
    for wechat mini app show information on Eshop
    """
    def get_object(self, pk):
        try:
            return Merchandise.objects.filter(categoryID=pk)
        except Merchandise.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        merchandises = self.get_object(pk)
        serializer = MerchandiseListShowInfoSerializer(merchandises, many=True)
        return Response(serializer.data)


class ShopListView(APIView):
    """
    List all the shop informations
    """
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopListShowInfoSerializer(shops, many=True)
        return Response(serializer.data)
#
# class CustomerViewSet(viewsets.ModelViewSet):
#     """
#         This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#     #                       IsOwnerOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class OwnerViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = OwnerSerializer
#
#
# class WxUserViewSet(viewsets.ModelViewSet):
#     queryset = WxUser.objects.all()
#     serializer_class = WxUserSerializer
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#
# @authentication_classes([])
# @permission_classes([])
# class ShopViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer
#
#
# class RackViewSet(viewsets.ModelViewSet):
#     queryset = Rack.objects.all()
#     serializer_class = RackSerializer
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all()
#     serializer_class = SupplierSerializer
#
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ESLViewSet(viewsets.ModelViewSet):
#     queryset = ESL.objects.all()
#     serializer_class = ESLSerializer
#
#
# class RFIDViewSet(viewsets.ModelViewSet):
#     queryset = RFID.objects.all()
#     serializer_class = RFIDSerializer
#
#
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer