# Stdlib imports
import time
from django.utils import timezone
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from customers.models import Customer
from orders.models import Order
from .serializers import CreateTopUpSerializer
from payments.models import PayOrderByWechat
from .models import TopUp
from payments.models import PayOrderByWechat, OrderQuery
from customers.serializers import DetailResponseSerializer


class TopUpView(APIView):
    """
    Topup to add user balance
    miniApp-balance.js

    Parameters:
        id - user uuid
        amountPay - need to user wechatPay to real pay
        amountAdd - extra free balance added

    Returns:
      payData - for miniApp to request a wechatPay

    Raises:
    """
    def post(self, request):

        wuser = Customer.objects.get(id=request.data.get('id'))
        openid = wuser.openid
        balance = wuser.balance
        timestamp = str(time.time())
        tradeNo = timestamp.replace('.', '0')

        data = {'userID': request.data.get('id'), 'tradeNo': tradeNo, 'amountPay': request.data.get('amountPay'), 'amountAdd': request.data.get('amountAdd')}
        serializer = CreateTopUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            payData = PayOrderByWechat(request.data.get('amountPay'), tradeNo, openid)
            if (payData==400):
                payData = {'status': 404}

        return Response(payData, status=status.HTTP_200_OK)


class TopUpSuccessView(APIView):
    """
    When wechatPay success, request for this Api,it will renew the order and user info, also query the tencent server to ensure the payment
    miniApp-user/banlance

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
        topuporder = TopUp.objects.get(tradeNo=request.data.get('tradeNo'))
        wuser = Customer.objects.get(id=request.data.get('id'))
        querydata = OrderQuery(request.data.get('tradeNo'))

        if querydata.get('status') == 200:
            topuporder.status = 1
            wuser.balance = wuser.balance + topuporder.amountPay +topuporder.amountAdd
            wuser.level = 1
            topuporder.paymentSN = querydata.get('transaction_id')
            topuporder.save()

        if querydata.get('status') == 400:
            return Response(400, status=status.HTTP_200_OK)

        wuser.save()
        serializer = DetailResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PointToBalanceView(APIView):
        """
        Transfer point to balance
        miniApp-user/point.js

        Parameters:
            id - user id
            balanceAdd -
            pointUse -

        Returns:
          id - user uuid
          point -
          level -
          balance -

        Raises:
        """
        def post(self, request):
            wuser = Customer.objects.get(id=request.data.get('id'))
            wuser.balance = wuser.balance + request.data.get('balanceAdd')
            wuser.point = wuser.point - request.data.get('pointUse')
            wuser.save()
            serializer = DetailResponseSerializer(wuser)
            return Response(serializer.data, status=status.HTTP_200_OK)