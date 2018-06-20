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
from .serializers import OrderListShowSerializer, CreateOrderSerializer, GetOrderDetailSerializer
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
        order_list = Order.objects.filter(userID=request.data['id'])
        wait_num = len(order_list.filter(status=0))
        process_num = len(order_list.filter(status=1))
        res = []
        res.append(wait_num)
        res.append(process_num)

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
        order_list = Order.objects.filter(userID=request.data['userID'])
        type_list = order_list.filter(status=request.data['status'])
        serializer = OrderListShowSerializer(type_list, many=True)
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
        :param order_method # 0 for online order, 1 for offline order
        :param user_id
        :param shop_id
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
        order_method = request.data.get('order_method')
        # 0 for online order, 1 for offline order
        user_id = request.data.get('user_id')
        shop_id = request.data.get('shop_id')
        if order_method == 0:
            address_id = request.data.get('address_id')
        else:
            address_id = None
        order_list = request.data.get('orderList')
        wuser = Customer.objects.get(pk=user_id)

        # set orderDetail list & calculate total price
        details = []
        total_num = 0
        total_price = 0
        delivery_fee = 0
        for order in order_list:
            merchandise = Merchandise.objects.get(id=order.get('id'))
            name = merchandise.name
            price_on_sold = merchandise.originPrice
            # set price for VIP customer
            # if userLevel == 1:
            #     priceOnSold = merchandise.clubPrice
            details.append({'merchandiseID': order.get('id'),
                            'merchandiseNum': order.get('num'),
                            'priceOnSold': float('%.2f' % price_on_sold),
                            })
            total_price = total_price + order.get('num')*float('%.2f' % price_on_sold)
            total_num = total_num + order.get('num')

        # prepare data for wechatPay
        timestamp = str(time.time())
        trade_no = timestamp.replace('.', '0') + str(user_id)

        total_price = float('%.2f' % total_price)
        # calculate the pay money
        if total_price > wuser.balance:
            pay_price = total_price - float('%.2f' % wuser.balance)
            pay_price = float('%.2f' % pay_price)
            available_balance = wuser.balance

        else:
            pay_price = 0
            available_balance = total_price

        # prepare data for serializer to create order
        if order_method == 0:
            orderdata = {'userID': user_id,
                         'shopID': shop_id,
                         'status': 0,
                         'paymentMethod': 'WaitForPay',
                         'tradeNo': trade_no,
                         'discount': 0,
                         'delivery': delivery_fee,
                         'totalPrice': total_price,
                         'balanceUse': available_balance,
                         'payPrice': pay_price,
                         'name': name,
                         'totalNum': total_num,
                         'comment': '',
                         'addressID': address_id,
                         'details': details,
                         }

        else:
            orderdata = {'userID': user_id,
                         'shopID': shop_id,
                         'status': 5,
                         'paymentMethod': 'WaitForPay',
                         'tradeNo': trade_no,
                         'discount': 0,
                         'delivery': 0.00,
                         'totalPrice': total_price,
                         'balanceUse': available_balance,
                         'payPrice': pay_price,
                         'name': name,
                         'totalNum': total_num,
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
                'tradeNo': trade_no,
            }
            return Response(res, status=status.HTTP_200_OK)
        print(serializer.errors)

        return Response('Order Create Error', status=status.HTTP_400_BAD_REQUEST)





