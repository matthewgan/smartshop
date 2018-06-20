# Stdlib imports
# Core Django imports
from django.utils import timezone
# Third-party app imports
# Imports from your apps
from orders.models import Order
from customers.serializers import CustomerPaymentResponseSerializer
from wechatpay.methods import wechat_pay, wechat_pay_qr_code
from alipay.methods import alipay_qr_code


def payment_with_wechat_online_order(trade_no, open_id):
    """
    :param trade_no:
    :param open_id:
    :return:
    SUCCESS
    {
        'status': success,
        'timeStamp': timestamp,
        'nonceStr': nonce_str,
        'package': package,
        'signType': 'MD5',
        'paySign': paysign,
        'tradeNo': out_trade_no,
    }

    FAILED
    {
        'status': fail,
        'error_msg' : error_msg
    }
    """
    order = Order.objects.get(tradeNo=trade_no)
    result = wechat_pay(order.payPrice, order.tradeNo, open_id)
    return result


def payment_qr_code_with_offline_order(trade_no, open_id):
    """
        :param trade_no:
        :param open_id:
        :return:
        SUCCESS
        {
            'status': 'success',
            'AliPayQRcodeUrl':
            'WechatPayQRcodeUrl':
        }
    """
    order = Order.objects.get(tradeNo=trade_no)
    fee = float('%.2f' % order.payPrice)

    # generate the QRcode for Alipay and Wechat pay
    alipay_code_url = alipay_qr_code(subject='物掌柜智慧便利', out_trade_no=trade_no, total_amount=fee)
    wechat_pay_code_url = wechat_pay_qr_code(fee, trade_no, open_id)

    res = {
        'status': 'success',
        'alipay_code_url': alipay_code_url,
        'wechat_pay_code_url': wechat_pay_code_url,
    }
    return res


def payment_with_balance(trade_no):
    """
    :param trade_no:
    :return:
    {
        'status' : 2,
        'balance': 'userBalance',
    }
    """
    res = {'status': 2}

    # get the data from database
    order = Order.objects.get(tradeNo=trade_no)
    wuser = order.userID

    # edit the database of order and customer
    order.status = 1
    order.payTime = timezone.now()
    order.paymentMethod = 'Balance'
    wuser.balance = wuser.balance - order.totalPrice

    # save database
    order.save()
    wuser.save()
    serializer = CustomerPaymentResponseSerializer(wuser)
    res['balance'] = serializer.data.get('balance')
    return res
