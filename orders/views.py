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
from .serializers import OrderListShowSerializer, CreateOrderSerializer, GetOrderDetailSerializer, OrderListForConfirmSerializer
from merchandises.models import Merchandise
from customers.models import Customer
from partnervoucher.models import PartnerVoucher
from partnerevent.models import PartnerEvent


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
            'code': 201,
            'tradeNo': tradeNo,
        }
        FAIL:
        {
            'code': 400,
            error_details
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
        if order_method == 0:
            delivery_fee = float('%.2f' % request.data.get('delivery'))

        for order in order_list:
            merchandise = Merchandise.objects.get(id=order.get('id'))
            name = merchandise.name
            code = merchandise.code
            price_on_sold = merchandise.originPrice
            # set price for VIP customer
            # if userLevel == 1:
            #     priceOnSold = merchandise.clubPrice
            details.append({'merchandiseID': order.get('id'),
                            'merchandiseNum': order.get('num'),
                            'priceOnSold': float('%.2f' % price_on_sold),
                            })
            total_price = total_price + order.get('num')*float('%.2f' % price_on_sold)
            total_price = float('%.2f' % total_price)
            total_num = total_num + order.get('num')

        # prepare data for wechatPay
        timestamp = str(time.time())
        trade_no = timestamp.replace('.', '0') + str(user_id)
        if order_method == 0:
            total_price = float('%.2f' % total_price) + delivery_fee

        # 判断优惠券使用条件
        voucher_list = PartnerVoucher.objects.filter(customer_id=request.data.get('user_id'))
        valid_voucher = voucher_list.filter(status=1)
        voucher_num = len(valid_voucher)
        discount = 0
        maxAmount = 0
        if voucher_num > 0:
            for voucher in valid_voucher:
                #voucher为自营券
                if voucher.event_id.type == 2:
                    #订单满足使用条件
                    if total_price >= voucher.event_id.order_min:
                        # 查找最大数额的可使用券
                        if voucher.event_id.discount_num > maxAmount:
                            maxAmount = voucher.event_id.discount_num
                            voucher.status = 0
                            voucher.save()
                            discount = maxAmount

        discount = float('%.2f' % discount)
        # calculate the pay money
        if total_price-discount > wuser.balance:
            pay_price = total_price - float('%.2f' % wuser.balance) - discount
            pay_price = float('%.2f' % pay_price)
            balanceUse = wuser.balance

        else:
            pay_price = 0
            balanceUse = total_price - discount

        # prepare data for serializer to create order
        if order_method == 0:
            orderdata = {'userID': user_id,
                         'shopID': shop_id,
                         'status': 0,
                         'paymentMethod': 'WaitForPay',
                         'tradeNo': trade_no,
                         'discount': discount,
                         'delivery': delivery_fee,
                         'totalPrice': total_price,
                         'balanceUse': balanceUse,
                         'payPrice': pay_price,
                         'name': name,
                         'code': code,
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
                         'discount': discount,
                         'delivery': 0.00,
                         'totalPrice': total_price,
                         'balanceUse': balanceUse,
                         'payPrice': pay_price,
                         'name': name,
                         'code': code,
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
                'msg': 'Create Order Success',
                'tradeNo': trade_no,
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckForNewOrderView(APIView):
    """
        商家查询系统- 订单获取
        获取所有状态为1（等待收货）的用户订单显示
        *参数：
    """
    def post(self, request):
        order_list = Order.objects.filter(status=1)
        serializer = OrderListForConfirmSerializer(order_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmOrderView(APIView):
    """
        商家查询系统- 确认订单按钮
        点击可以将订单状态从1（等待收货）更改为2（订单完成）
        *参数： tradeNo
    """
    def post(self, request):
        order = Order.objects.get(tradeNo=request.data.get('tradeNo'))
        order.status = 2
        order.save()
        return Response(status=status.HTTP_202_ACCEPTED)



