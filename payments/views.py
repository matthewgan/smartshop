# Stdlib imports
# Core Django imports
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Third-party app imports
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from payments.models import PayOrderByWechat
from customers.models import Customer
from customers.serializers import DetailResponseSerializer
from orders.models import Order
from payments.models import PayOrderOnline, PayOrderOffline, PayOrderWithBalance, MiniAppOrderQuery
from payments.models import trans_xml_to_dict, trans_dict_to_xml


@permission_classes((AllowAny, ))
class GetTencentNotifyView(APIView):
    def post(self, request):
        msg = request.text.encode('ISO-8859-1').decode('utf-8')
        res = trans_xml_to_dict(msg)

        if res.get('return_code')=='SUCCESS':
            if res.get('result_code')=='SUCCESS':
                tradeNo = res.get('out_trade_no')
                order = Order.objects.get(tradeNo=tradeNo)
                wuser = order.userID
                order.status = 3
                wuser.point = wuser.point + order.payPrice * 100
                order.paymentSN = res.get('transaction_id')
                order.payTime = timezone.now()
                order.paymentMethod = 'Wechat_Pay_In_Store'
                order.save()
            else:
                error_code = res.get('err_code')
                error_mes = res.get('err_code_des')
                print(error_code, error_mes)
        else:
            error_mes = res.get('return_msg')
            print(error_mes)


        res = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK',
        }

        resxml = trans_dict_to_xml(res)
        return Response(resxml, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class GetAlipayNotifyView(APIView):
    def post(self, request):


        if request.get('trade_status') == '交易支付成功':
            tradeNo = request.get('out_trade_no')
            order = Order.objects.get(tradeNo=tradeNo)
            wuser = order.userID
            order.status = 3
            wuser.point = wuser.point + order.payPrice * 100
            order.paymentSN = request.get('trade_no')
            order.payTime = timezone.now()
            order.paymentMethod = 'Alipay_Pay_In_Store'
            order.save()
        else:
            trade_status = request.get('trade_status')
            print(trade_status)

        return Response('SUCCESS', status=status.HTTP_200_OK)


class paytest(APIView):

    def post(self,request):
        tn = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        return Response('ok', status=status.HTTP_200_OK)


class PayOrderPreProcess(APIView):
    """
    :param orderType
    :param userID
    :param tradeNo

    :return:
    orderMethod == 0 (online pay)
    SUCCESS
    {
        'timeStamp': timestamp,
        'nonceStr': nonce_str,
        'package': package,
        'signType': 'MD5',
        'paySign': paysign,
        'tradeNo': out_trade_no,
        'status': 1 # pay by ali/wechat
    }
    FAILED
    {
        'status' : 404
    }
    -------------------------------------
    orderMethod == 1 (offline pay)
    SUCCESS
    {
        'AliPayQRcodeUrl': timestamp,
        'WechatPayQRcodeUrl': nonce_str,
        'status': 1 # pay by ali/wechat
    }
    FAILED
    {
        'status' : 404
    }
    -------------------------------------
    balance payment (balance pay)
    {
        'status' : 2, # pay with balance
        'balance': 'userBalance',
    }
    """
    def post(self, request):
        # get data from request
        orderMethod = request.data.get('orderMethod')
        userID = request.data.get('userID')
        tradeNo = id=request.data.get('tradeNo')

        # get userInfo from database
        wuser = Customer.objects.get(pk=userID)
        userLevel = wuser.level
        userBalance = float('%.2f' % wuser.balance)
        openID = wuser.openid

        # get orderInfo from database
        order = Order.objects.get(tradeNo=tradeNo)

        # calculate the pay money and determin the method of payments
        if order.payPrice > 0:  # user Alipay or WechatPay
            wuser.balance = 0
            wuser.save()
            if orderMethod == 0:  # user WechatPay within miniApp
                res = PayOrderOnline(tradeNo, openID)
            if orderMethod == 1:  # offline order
                res = PayOrderOffline(tradeNo, openID)
        else:
            # complete pay if balance is enough to pay

            res = PayOrderWithBalance(tradeNo)

        return Response(res, status=status.HTTP_200_OK)


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
        querydata = MiniAppOrderQuery(request.data.get('tradeNo'))

        if querydata.get('status') == 200:
            order.status = 1
            wuser.point = wuser.point + order.payPrice*100
            order.paymentSN = querydata.get('transaction_id')
            order.payTime = timezone.now()
            order.paymentMethod = 'Wechat Pay'
            order.save()

        if querydata.get('status') == 400:
            return Response(400, status=status.HTTP_200_OK)

        wuser.save()
        serializer = DetailResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)