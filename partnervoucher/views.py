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
    当线上或者线下完成符合条件的订单时（成功），访问此API获取目前存在的促销信息，并且判断用户及付款金额是否符合获取条件，如有符合条件的选项，创建一个新voucher

    Parameters:
        user_id - user uuid
        trade_no - the tradeNo of selected order

    Returns:
      new_voucher: 创建成功优惠券的数量

    Raises:
    """
    def post(self, request):

        order = Order.objects.get(tradeNo=request.data.get('trade_no'))
        wuser = Customer.objects.get(id=request.data.get('user_id'))

        voucher_list = PartnerVoucher.objects.filter(customer_id=request.data.get('user_id'))
        event_list = PartnerEvent.objects.filter(status=1)

        print_res = []
        new_voucher = 0

        if len(event_list) > 0:
            for event in event_list:
                try:
                    voucherNum = len(voucher_list.filter(event_id=event.id))
                except:
                    voucherNum = 0

                if event.limit > voucherNum:
                    if wuser.level >= event.customer_level:
                        if order.totalPrice >= event.payment_min:
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
                                print_res.append(pring_data)
                                new_voucher = new_voucher+1

                        else:
                            pring_data = {
                                'err_code': 1201,
                                'event': event.name,
                                'err_msg': '消费没有达到获取条件'
                            }
                            print_res.append(pring_data)
                    else:
                        pring_data = {
                            'err_code': 1202,
                            'event': event.name,
                            'err_msg': '用户等级不符合领券要求'
                        }
                        print_res.append(pring_data)
                else:
                    pring_data = {
                        'err_code': 1203,
                        'event': event.name,
                        'err_msg': '该用户领券数达到上限'
                    }
                    print_res.append(pring_data)
        else:
            print_res = {
                'err_code': 1000,
                'err_msg': '没有进行中的送券活动'
            }
        print(print_res)

        return Response(new_voucher, status=status.HTTP_201_CREATED)


class ShowVoucherView(APIView):
    """
    用户在小程序"我的"页面"优惠券"选项卡中查看当前有效优惠券

    Parameters:
        id - user uuid

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
        print(voucher_list)
        valid_voucher = voucher_list.filter(status=1)
        voucher_num = len(valid_voucher)
        res = []
        if voucher_num > 0:
            serializer = ShowVoucherSerializer(valid_voucher, many=True)
            res = serializer.data

        return Response(res, status=status.HTTP_200_OK)


class ShowVoucherView(APIView):
    """
    用户在小程序"我的"页面"优惠券"选项卡中查看当前有效优惠券

    Parameters:
        id - user uuid

    Returns:
      res = [
        {
            'code':
            'event_name':
            'partner_name':
            'end_time':
            'content':
        },
        {
            'code':
            'event_name':
            'partner_name':
            'end_time':
            'content':
        },
        ...
      ]

    Raises:
    """
    def post(self, request):

        voucher_list = PartnerVoucher.objects.filter(customer_id=request.data.get('user_id'))
        valid_voucher = voucher_list.filter(status=1)
        voucher_num = len(valid_voucher)
        res = []
        if voucher_num > 0:
            serializer = ShowVoucherSerializer(valid_voucher, many=True)
            res = serializer.data

        return Response(res, status=status.HTTP_200_OK)


class VerifyVoucherView(APIView):
    """
    用户在小程序"我的"页面"优惠券"选项卡中可以点击核销按钮完成优惠券核销

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