# Stdlib imports
import time
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from customers.models import Customer
from .serializers import CreateTopUpSerializer, TopUpGiftSerializer, TopUpSuccessSerializer
from .models import TopUp, TopUpGift
from wechatpay.methods import wechat_pay, wechat_pay_query
from customers.serializers import CustomerPaymentResponseSerializer


def calculate_gift(input_value):
    """
    claculate how much gift should give when customer pay for topup
    :param input_value:
    :return:
    """
    input_topup = input_value
    output_gift = 0
    rule = TopUpGift.objects.latest('timestamp')
    while input_topup - rule.level5topup >= 0:
        input_topup -= rule.level5topup
        output_gift += rule.level5gift
    if input_topup - rule.level4topup >= 0:
        input_topup -= rule.level4topup
        output_gift += rule.level4gift
    if input_topup - rule.level3topup >= 0:
        input_topup -= rule.level3topup
        output_gift += rule.level3gift
    if input_topup - rule.level2topup >= 0:
        input_topup -= rule.level2topup
        output_gift += rule.level2gift
    if input_topup - rule.level1topup >= 0:
        input_topup -= rule.level1topup
        output_gift += rule.level1gift
    if input_topup - rule.level0topup >= 0:
        input_topup -= rule.level0topup
        output_gift += rule.level0gift
    return output_gift


class TopupCreateView(APIView):
    """Generate Top up order and call payment method"""
    def post(self, request):
        serializer = CreateTopUpSerializer(data=request.data)
        if serializer.is_valid():
            topup = serializer.save()
            timestamp = str(time.time())
            topup.tradeNo = timestamp.replace('.', '0') + str(topup.id)
            topup.amountAdd = calculate_gift(topup.amountPay)
            topup.save()
            result = wechat_pay(topup.amountPay, topup.tradeNo, topup.userID.openid)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = TopUpSuccessSerializer(data=request.data)
        if serializer.is_valid():
            tradeNo = serializer.validated_data.get('tradeNo')
            topup = TopUp.objects.get(tradeNo=tradeNo)
            querydata = wechat_pay_query(topup.tradeNo)
            if querydata.get('status') == 200:
                topup.status = 1
                topup.paymentSN = querydata.get('transaction_id')
                topup.userID.level = 1
                topup.userID.balance += topup.amountPay + topup.amountAdd
                topup.userID.save()
                topup.save()
                output_serializer = CustomerPaymentResponseSerializer(topup.userID)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(querydata, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class checkTopUpView(APIView):

    def post(self, request):
        topup_list = TopUp.objects.filter(userID=request.data['id'])
        wait_for_pay_list = topup_list.filter(status=0)
        checkNo = 0
        for topup in wait_for_pay_list:
            querydata = wechat_pay_query(topup.tradeNo)
            if querydata.get('status') == 200:
                topup.status = 1
                topup.paymentSN = querydata.get('transaction_id')
                topup.userID.level = 1
                topup.userID.balance += topup.amountPay + topup.amountAdd
                topup.userID.save()
                topup.save()
                checkNo = checkNo + 1
 
        return Response(checkNo, status=status.HTTP_200_OK)


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
            serializer = CustomerPaymentResponseSerializer(wuser)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ShowGiftView(APIView):
    """
    Get Top Up Gift from wechat, Show gift rules on screen
    """
    def get(self, request):
        gift = TopUpGift.objects.latest('timestamp')
        serializer = TopUpGiftSerializer(gift)
        return Response(serializer.data, status=status.HTTP_200_OK)
