from django.shortcuts import render
# Third-party app imports
from rest_framework.views import APIView
import random
import time
import datetime
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from customers.models import Customer
from customers.serializers import CustomerPaymentResponseSerializer
from orders.models import Order
from partnerevent.models import PartnerEvent
from partnervoucher.models import PartnerVoucher
from .serializers import CreateVoucherSerializer, ShowVoucherSerializer
# Create your views here.


class CreateVoucherView(APIView):
    """
    创建优惠券/红包接口

    1. 当线上或者线下完成符合条件的订单时（成功），访问此API获取目前存在的促销信息，并且判断用户及付款金额是否符合获取条件，如有符合条件的选项，创建一个新voucher
    2. 无需消费时可调用此接口，判断用户是否符合发放优惠券的条件，如符合要求 创建一个新voucher

    Parameters:
        *user_id - user uuid
        trade_no - the tradeNo of selected order（无需消费条件时可以为空）

    Returns:
      new_voucher: 创建成功优惠券的数量

    Raises:
    """
    def post(self, request):

        wuser = Customer.objects.get(id=request.data.get('user_id'))

        # 用户当前优惠券(包括使用和过期)
        voucher_list = PartnerVoucher.objects.filter(customer_id=request.data.get('user_id'))

        # 当前可用活动
        event_list = PartnerEvent.objects.filter(status=1)


        new_voucher = 0

        if len(event_list) > 0:

            # 对每一个活动进行条件判断
            for event in event_list:
                # 计算当前活动用户拥有券数量
                try:
                    voucherNum = len(voucher_list.filter(event_id=event.id))
                except:
                    voucherNum = 0

                # 判断是否需要订单消费
                try:
                    order = Order.objects.get(tradeNo=request.data.get('trade_no'))
                    totalPrice = order.totalPrice
                except:
                    totalPrice = 0;

                # 判断用户是否达到领券上限
                if event.limit > voucherNum:
                    # 判断用户是否达到领取等级
                    if wuser.level >= event.customer_level:
                        # 判断用户消费是否达标 && 事件为无需消费事件
                        if totalPrice >= event.payment_min:
                            code = str(event.partner_id.code) + str(random.randint(0, 99999)).zfill(5) + str(
                                int(time.time()))
                            valid_days = datetime.timedelta(days=event.voucher_valid_time)
                            end_date = event.start_time + valid_days
                            data = {
                                'code': code,
                                'event_id': event.id,
                                'customer_id': wuser.id,
                                'end_time': end_date,
                            }
                            serializer = CreateVoucherSerializer(data=data)

                            if serializer.is_valid():
                                serializer.save()
                                pring_data = serializer.data
                                pring_data['err_code'] = 1000
                                pring_data['err_msg'] = '成功创建一张优惠券'
                                new_voucher = new_voucher+1


        return Response(new_voucher, status=status.HTTP_201_CREATED)


class ShowVoucherView(APIView):
    """
    用户在小程序"我的"页面"优惠券"选项卡中查看当前有效优惠券
    或者在我的红包中显示有效折扣券

    Parameters:
        id - user uuid
        type - event type

    Returns:
      res = [
        {
            'code':
            'event_name':
            'partner_name':
            'end_time':
            'content':
            'area':
        },
        {
            'code':
            'event_name':
            'partner_name':
            'end_time':
            'content':
            'area':
        },
        ...
      ]

    Raises:
    """
    def post(self, request):

        voucher_list = PartnerVoucher.objects.filter(customer_id=request.data.get('user_id'))
        type = request.data.get('type')

        valid_voucher = voucher_list.filter(status=1)
        voucher_num = len(valid_voucher)
        res = []
        display_voucher = []
        if voucher_num > 0:
            for voucher in valid_voucher:
                if voucher.event_id.type == type:
                    display_voucher.append(voucher)
            serializer = ShowVoucherSerializer(display_voucher, many=True)
            res = serializer.data

        return Response(res, status=status.HTTP_200_OK)


class VerifyVoucherView(APIView):
    """
    用户在小程序"我的"页面"优惠券"选项卡中可以点击核销按钮完成优惠券核销
    或者在我的红包页面中完成核销（店面线下支付没有通过收银仓结算时使用）

    Parameters:
        code - 优惠券code

    Returns:
      Success info

    Raises:
    """
    def post(self, request):

        voucher = PartnerVoucher.objects.get(code=request.data.get('code'))
        voucher.status = 0
        voucher.save()
        res = {
            'err_code': '0000',
            'err_msg': 'SUCCESS',
        }

        return Response(res, status=status.HTTP_200_OK)


class VerifyVoucherWithMiniAppPaymentView(APIView):
    """
    用户在小程序下单时，调用此接口查看可用的红包抵扣

    Parameters:
        id - user uuid

    Returns:
      res = [
        {
            order_min:(使用支付条件)
            discount:(抵扣金额)
        },
        {
            order_min:(使用支付条件)
            discount:(抵扣金额)
        }
      ]

    Raises:
    """
    def post(self, request):

        voucher_list = PartnerVoucher.objects.filter(customer_id=request.data.get('user_id'))
        valid_voucher = voucher_list.filter(status=1)
        voucher_num = len(valid_voucher)
        res_list = [];
        if voucher_num > 0:
            for voucher in valid_voucher:
                if voucher.event_id.type != 1:
                        res = {
                            'order_min': voucher.event_id.order_min,
                            'discount': voucher.event_id.discount_num,
                        }
                        res_list.append(res);

        return Response(res_list, status=status.HTTP_200_OK)