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
from payments.models import PayOrderByWechat, OrderQuery
from customers.serializers import DetailResponseSerializer


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
        order.cancelTime = timezone.now();
        order.save()
        return Response('ok', status=status.HTTP_200_OK)


class SubmitOrderView(APIView):
    """
    Create order in model and get data from Tencent server send to miniApp for WechatPay
    miniApp-.cart/index.js

    Parameters:
        userID - user id
        shopID -
        addressID -
        orderList -

    Returns:
      payData
      -WeChatPay package(when need wechatpay)
      -success payInfo & new balance

    Raises:
    """
    def post(self, request):

        # get data from request
        userID = request.data.get('userID')
        shopID = request.data.get('shopID')
        addressID = request.data.get('addressID')
        orderList = request.data.get('orderList')

        # get userInfo from database
        wuser = Customer.objects.get(id=userID)
        userLevel = wuser.level
        userBalance = float('%.2f' % wuser.balance)
        openID = wuser.openid

        # set orderDetail list & calculate total price
        details = []
        totalNum = 0
        totalPrice = 0
        for order in orderList:
            merchandise = Merchandise.objects.get(id=order.get('id'))
            name = merchandise.name
            priceOnSold = merchandise.originPrice
            # set price for VIP customer
            # if userLevel == 1:
            #     priceOnSold = merchandise.clubPrice
            details.append({'merchandiseID': order.get('id'), 'merchandiseNum': order.get('num'), 'priceOnSold': float('%.2f' % priceOnSold)})
            totalPrice = totalPrice + order.get('num')*float('%.2f' % priceOnSold)
            totalNum = totalNum + order.get('num')

        # prepare data for wechatPay
        timestamp = str(time.time())
        tradeNo = timestamp.replace('.','0')
        if totalPrice > userBalance:
            payPrice = totalPrice-userBalance
            balanceUse = userBalance
        else:
            payPrice = 0
            balanceUse = totalPrice
        payPrice = float('%.2f' % payPrice)
        balanceUse = float('%.2f' % balanceUse)

        # prepare data for serializer to create order
        orderdata = {'userID': userID, 'shopID': shopID, 'status': 0, 'paymentMethod': 'weChatPay', 'tradeNo': tradeNo, 'discount': 0, 'delivery': 5, 'totalPrice': totalPrice, 'balanceUse': balanceUse, 'payPrice': payPrice, 'name': name, 'totalNum': totalNum, 'comment': '', 'addressID': addressID, 'details': details}

        # save to database
        serializer = CreateOrderSerializer(data=orderdata)

        if serializer.is_valid():
            serializer.save()

            # get data for wechatPay if need to pay
            if totalPrice > userBalance:
                payData = PayOrderByWechat(payPrice, tradeNo, openID)
                if (payData == 400):
                    payData = {'status':404}
                    return Response(payData, status=status.HTTP_200_OK)
                wuser.balance = 0
                wuser.save()
                payData['status'] = 1
            else:
                # complete pay if balance is enough to pay
                payData = {'status': 2}
                order = Order.objects.get(tradeNo=tradeNo)
                order.status = 1
                order.payTime = timezone.now()
                wuser.balance = float('%.2f' %wuser.balance) - totalPrice
                print(wuser.balance)
                order.save()
                wuser.save()
                serializer = DetailResponseSerializer(wuser)
                payData['balance'] = serializer.data.get('balance')

        else:
            print(serializer.errors)
            payData = {'status':400}
            return Response(payData, status=status.HTTP_200_OK)

        return Response(payData, status=status.HTTP_200_OK)


class PayOrderView(APIView):
    """
        To finish payment on order page (for order that status is 0)
        miniApp-order.js & detail.js

        Parameters:
            id - order id
            userId - user id

        Returns:
                id - user uuid
          point -
          level -
          balance -

        Raises:
        """

    def post(self, request):

        # get data from request
        print(request.data.get('id'))
        order = Order.objects.get(id=request.data.get('id'))
        wuser = Customer.objects.get(id=request.data.get('userId'))
        if order.payPrice == 0:
            order.status = 1
            order.payTime = timezone.now()
            order.save()
            serializer = DetailResponseSerializer(wuser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            payData = PayOrderByWechat(order.payPrice, order.tradeNo, wuser.openid)
            if (payData==400):
                payData = {'status': 404}
            return Response(payData, status=status.HTTP_200_OK)

class PaySuccessView(APIView):
    """
    When wechatPay success, request for this Api,it will renew the order and user info, also query the tencent server to ensure the payment
    miniApp-cart/index.js & balance.js & order.js & detail.js

    Parameters:
        id - user uuid
        tradeNo - the tradeNo of selected order

    Returns:
      id - user uuid
      point -
      level -
      balance -

    Raises:
    """
    def post(self, request):
        order = Order.objects.get(tradeNo=request.data.get('tradeNo'))
        wuser = Customer.objects.get(id=request.data.get('id'))
        querydata = OrderQuery(request.data.get('tradeNo'))

        if querydata.get('status') == 200:
            order.status = 1
            wuser.point = wuser.point + order.payPrice*100
            order.paymentSN = querydata.get('transaction_id')
            order.payTime = timezone.now()
            order.save()

        if querydata.get('status') == 400:
            return Response(400, status=status.HTTP_200_OK)

        wuser.save()
        serializer = DetailResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)


