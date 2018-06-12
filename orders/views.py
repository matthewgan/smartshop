# Stdlib imports
# Core Django imports
from django.utils import timezone
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time

# Imports from your apps
from .models import Order, OrderDetail
from .serializers import OrderListShowSerializer, CreateOrderSerializer, \
    WeChatPayOrderSerializer, GetOrderDetailSerializer
from merchandises.models import Merchandise
from customers.models import Customer


class GetOrderNumView(APIView):
    """
    Get order number for different type(waitForPay and Inprocess)
    miniApp-user.js

    Parameters:
        id = user uuid

    Returns:
      waitNum - order status0
      processNum - order status1

    Raises:
    """
    def post(self, request):
        orderList = Order.objects.filter(userID=request.data['id'])
        waitNUm = len(orderList.filter(status=0))
        processNum = len(orderList.filter(status=1))
        res = []
        res.append(waitNUm)
        res.append(processNum)

        return Response(res, status=status.HTTP_200_OK)


class GetOrderListView(APIView):
    """
    Get order list for different type of order status
    miniApp-order.js

    Parameters:
        userID = user uuid
        status = type of order

    Returns:
      'id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery',
      'totalPrice', 'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'createTime',
      'cancelTime', 'tradeNo'
      Of select status of order

    Raises:
    """
    def post(self, request):

        orderList = Order.objects.filter(userID=request.data['userID'])
        typeList = orderList.filter(status=request.data['status'])
        serializer = OrderListShowSerializer(typeList, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOderDetailView(APIView):
    """
    Show the detail info of a selected order
    miniApp-detail.js

    Parameters:
        uuid = user uuid
        imgFile = user face file

    Returns:
      'id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery', 'totalPrice',
      'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'details', 'createTime', 'addName',
      'addTel', 'addDetail'

    Raises:
    """
    def post(self, request):

        order = Order.objects.get(id=request.data['id'])
        serializer = GetOrderDetailSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelOrderView(APIView):
    """
    Cancel order to change the status from 0 to 4
    miniApp-detail.js & order.js

    Parameters:
        id = order id
        userId = user id, to returen the balance bace to user_balance

    Returns:
      'ok' - cancel success

    Raises:
    """
    def post(self, request):

        order = Order.objects.get(id=request.data['id'])
        wuser = Customer.objects.get(id=request.data['userId'])
        wuser.balance = order.balanceUse
        wuser.save()
        order.status = 4
        order.cancelTime = timezone.now()
        order.save()
        return Response('ok', status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    """
        :param orderMethod # 0 for online order, 1 for offline order
        :param userID
        :param shopID
        :param orderList(
            {'id':1, 'num':1),
            {'id':2, 'num':2)
        )
        :return:
        SUCCESS:
        {
            'code': 200,
            'tradeNo': tradeNo,
        }
        FAIL:
        {
            'code': 201,
            'Order Create Error'
        {
    """
    def post(self, request):
        # get data from request
        orderMethod = request.data.get('orderMethod') # 0 for online order, 1 for offline order
        userID = request.data.get('userID')
        shopID = request.data.get('shopID')
        if orderMethod == 0:
            addressID = request.data.get('addressID')
        orderList = request.data.get('orderList')

        # set orderDetail list & calculate total price
        details = []
        totalNum = 0
        totalPrice = 0
        deliveryFee = 0
        for order in orderList:
            merchandise = Merchandise.objects.get(id=order.get('id'))
            name = merchandise.name
            priceOnSold = merchandise.originPrice
            # set price for VIP customer
            # if userLevel == 1:
            #     priceOnSold = merchandise.clubPrice
            details.append({'merchandiseID': order.get('id'),
                            'merchandiseNum': order.get('num'),
                            'priceOnSold': float('%.2f' % priceOnSold),
                            })
            totalPrice = totalPrice + order.get('num')*float('%.2f' % priceOnSold)
            totalNum = totalNum + order.get('num')

        # prepare data for wechatPay
        timestamp = str(time.time())
        tradeNo = timestamp.replace('.','0') + str(userID)

        # prepare data for serializer to create order
        if orderMethod == 0:
            orderdata = {'userID': userID,
                         'shopID': shopID,
                         'status': 0,
                         'paymentMethod': 'WaitForPay',
                         'tradeNo': tradeNo,
                         'discount': 0,
                         'delivery': deliveryFee,
                         'totalPrice': totalPrice,
                         'balanceUse': 0.00,
                         'payPrice': 0.00,
                         'name': name,
                         'totalNum': totalNum,
                         'comment': '',
                         'addressID': addressID,
                         'details': details,
                         }

        else:
            orderdata = {'userID': userID,
                         'shopID': shopID,
                         'status': 5,
                         'paymentMethod': 'WaitForPay',
                         'tradeNo': tradeNo,
                         'discount': 0,
                         'delivery': 0.00,
                         'totalPrice': totalPrice,
                         'balanceUse': 0.00,
                         'payPrice': 0.00,
                         'name': name,
                         'totalNum': totalNum,
                         'comment': '',
                         'addressID': 1,
                         'details': details,
                         }
        # save to database
        serializer = CreateOrderSerializer(data=orderdata)

        if serializer.is_valid():
            serializer.save()
            res = {
                'code': 200,
                'tradeNo': tradeNo,
            }
            return Response(res, status=status.HTTP_200_OK)

        return Response('Order Create Error', status=status.HTTP_200_OK)





