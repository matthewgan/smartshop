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
import base64
from SmartShop.settings import *
import json
from rest_framework.decorators import authentication_classes, permission_classes
#import uuid
from django.http import JsonResponse
from django.http import Http404
from api.extendapi import *
import random


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
            wxapp_secret = 'a1573bde5e2d7768081d724aa44682e2'
            wxapp_appid = 'wx23c4e200139a74ee'
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
    3.1.3 upload code
    """
    def put(self, request, format=None):
        pk = request.data['id']
        wuser = WUser.objects.get(pk=pk)
        serializer = WUserSetCodeRequestSerializer(wuser, data=request.data)
        if serializer.is_valid():
            wuser = serializer.save()
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
        catgory = Category.objects.all()
        output_serializer = CategoryResponseSerializer(catgory, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


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


class RegisterFaceView(APIView):

    def post(self, request):
        serializer = UploadedFaceSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            uploadface = serializer.save()
        output_serializer = UploadedFaceSerializer(uploadface)
        imgUrl = output_serializer.data.get('image')
        imgRoot = MEDIA_ROOT + imgUrl[6:]

        # encode img to base64
        print(imgRoot)
        file = open(imgRoot, 'rb')
        img64 = base64.b64encode(file.read())

        # connect to baidu face api
        client = createapiface()
        detectRes = detectface(img64, 'BASE64', client)
        print(detectRes)

        # detect success -> rigister face
        if detectRes == 200:
           groupid = 'customer'
           userid = output_serializer.data.get('uuid')
           registerres = registerface(img64, 'BASE64', userid, groupid, client)
           print('------------------------------')

        return Response(detectRes, status=status.HTTP_200_OK)


class SearchUserFaceView(APIView):

    def post(self, request):
        serializer = SearchFaceUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploadface = serializer.save()
            output_serializer = SearchFaceUploadSerializer(uploadface)
            imgUrl = output_serializer.data.get('image')
            imgRoot = MEDIA_ROOT + imgUrl[6:]

            # encode img to base64
            print(imgRoot)
            file = open(imgRoot, 'rb')
            img64 = base64.b64encode(file.read())

            # connect to baidu face api
            client = createapiface()
            detectRes = detectface(img64, 'BASE64', client)

            if detectRes == 200:
                searchres = searchface(img64, 'BASE64', client)
                if searchres.get('status') == 200:
                    wuser = WUser.objects.get(id=searchres.get('userid'))
                    output_serializer = EntranceGetInfoResponseSerializer(wuser)
                    return Response(output_serializer.data, status=status.HTTP_200_OK)

            return Response(searchres, status=status.HTTP_200_OK)


class EntranceGetUserInfoView(APIView):

    def post(self, request):
        serializer = EntranceGetInfoRequestSerializer(data=request.data)
        if serializer.is_valid():
            wuser = WUser.objects.get(code=serializer.data.get('code'))
            output_serializer = EntranceGetInfoResponseSerializer(wuser)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOrderListView(APIView):

    def post(self, request):

        orderList = Order.objects.filter(userID=request.data['userID'])
        typeList = orderList.filter(status=request.data['status'])
        serializer = OrderListShowSeralizer(typeList, many=True)
        #print(serializer.data[0].get('id'))
        #print(serializer.data.__len__())
        #len = serializer.data.__len__()
        #ii = 0
        #while len > ii:
        #    orderDetail = OrderDetail.objects.filter(id=serializer.data[ii].ger('id'))
        #    detailSerializer = OrderDetailListSerializer(orderDetail, many=True)
        #    ij = 0
        #    detailLen = detailSerializer.data.__len__()
        #    while detailLen > ij:
        #        productList = Merchandise.objects.filter(merchandiseID=detailSerializer.data[ij].get('merchandiseID'))
        #        productListSerializer = OrderListProductInfoSerializer(productList, many=True)
        #        productListSerializer[0]
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitOrderView(APIView):

    def post(self, request):

        userID = request.data.get('userID')
        shopID = request.data.get('shopID')
        shop = Shop.objects.get(id=shopID)
        wuser = WUser.objects.get(id=userID)
        adress = Address.objects.get(id=1)
        orderList = request.data.get('orderList')
        print(orderList[0].get('num'))

        order = Order.objects.create(userID=wuser, shopID=shop, status=0, paymentMethod='weChatPay', paymentSN='', discount=0, delivery=5, bill=100, comment='', addressID=adress)
        i = 0
        while len(orderList) > i:
            merchandise = Merchandise.objects.get(id=orderList[i].get('id'))
            OrderDetail.objects.create(order=order, merchandiseID=merchandise, merchandiseNum=orderList[i].get('num'))
            i = i+1
        serializer = CreateOrderSerializer(instance=order)
        print(serializer.data)

        serializer = CreateOrderSerializer(data=orderList)
        print(serializer.initial_data)
        if serializer.is_valid():
            newOrder = serializer.save()

        return Response('ok', status=status.HTTP_200_OK)


class PayOrderByWechatView(APIView):

    def post(self, request):

        order = Order.objects.get(paymentSN=request.data.get('paymentSN'))
        serializer = WeChatPayOrderSeralizer(order)
        res = serializer.data
        PayOrderByWechat('1', res['paymentSN'], 'oh5IA5UJYYJWtBStjEp53N-7aom0')
        return Response('ok', status=status.HTTP_200_OK)


def isoformat(time):
    '''
    将datetime或者timedelta对象转换成ISO 8601时间标准格式字符串
    :param time: 给定datetime或者timedelta
    :return: 根据ISO 8601时间标准格式进行输出
    '''
    if isinstance(time, datetime.datetime): # 如果输入是datetime
        return time.isoformat();
    elif isinstance(time, datetime.timedelta): # 如果输入时timedelta，计算其代表的时分秒
        hours = time.seconds // 3600
        minutes = time.seconds % 3600 // 60
        seconds = time.seconds % 3600 % 60
        return 'P%sDT%sH%sM%sS' % (time.days, hours, minutes, seconds) # 将字符串进行连接

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