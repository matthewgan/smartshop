# Stdlib imports
import time
import random
import socket
import datetime
import requests
# Core Django imports
from django.utils import timezone
from django.db import models
# Third-party app imports
import hashlib
# Imports from your apps
from orders.models import Order
from customers.serializers import DetailResponseSerializer
from .methods import get_wechat_app_id, get_wechat_mch_id, get_wechat_sub_mch_id, get_wechat_sub_app_id
from .methods import get_host_ip, get_service_api_key, get_notify_url, get_tencent_unified_order_api
from .methods import trans_dict_to_xml, trans_xml_to_dict


class PaymentRecord(models.Model):
    app_id = models.CharField(max_length=20, default=get_wechat_app_id())
    mch_id = models.CharField(max_length=12, default=get_wechat_mch_id())
    sub_mch_id = models.CharField(max_length=12, default=get_wechat_sub_mch_id())
    sub_app_id = models.CharField(max_length=20, default=get_wechat_sub_app_id())
    sub_open_id = models.CharField(max_length=30)
    body = models.CharField(max_length=200, default='物掌柜智慧便利')
    nonce_str = models.CharField(max_length=10, default=str(int(random.random()*1e10)))
    notify_url = models.CharField(max_length=200, default=get_notify_url())
    out_trade_no = models.CharField(max_length=20)
    spbill_create_ip = models.CharField(max_length=20, default=get_host_ip())
    total_fee = models.CharField(max_length=20)
    sign = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=time.time())

    def create_record(self, open_id, trade_no, total_fee):
        record = self.create(sub_open_id=open_id, out_trade_no=trade_no, total_fee=total_fee)
        return record

    def get_str_for_sign(self):
        sign_string = "appid=" + str(self.app_id) \
                      + "&body=" + str(self.body) \
                      + "&mch_id=" + str(self.mch_id) \
                      + "&nonce_str=" + str(self.nonce_str) \
                      + "&notify_url=" + str(self.notify_url) \
                      + "&out_trade_no=" + str(self.out_trade_no) \
                      + "&spbill_create_ip=" + str(self.spbill_create_ip) \
                      + "&sub_appid=" + str(self.sub_app_id) \
                      + "&sub_mch_id=" + str(self.sub_mch_id) \
                      + "&sub_openid=" + str(self.sub_open_id) \
                      + "&total_fee=" + str(self.total_fee) \
                      + "&trade_type=JSAPI" \
                      + "&key=" + get_service_api_key()
        return sign_string

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        sign_str = self.get_str_for_sign()
        self.sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
        super(PaymentRecord, self).save(force_update=force_update)

    def model_to_dict(self):
        model_dict = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'sub_mch_id': self.sub_mch_id,
            'sub_appid': self.sub_app_id,
            'sub_openid': self.sub_open_id,
            'body': self.body,
            'nonce_str': self.nonce_str,
            'notify_url': self.notify_url,
            'out_trade_no': self.out_trade_no,
            'spbill_create_ip': self.spbill_create_ip,
            'total_fee': self.total_fee,
            'trade_type': 'JSAPI',
            'sign': self.sign,
        }
        return model_dict

    def __str__(self):
        return self.out_trade_no


def PayOrderByWechat(fee, out_trade_no, openid):
    # static data need to be put in setting
    appid = get_wechat_app_id()
    sub_appid = get_wechat_sub_app_id()
    sub_mchid = get_wechat_sub_mch_id()
    mch_id = get_wechat_mch_id()
    api_key = get_service_api_key()
    notify_url = get_notify_url()
    tencent_unifiedorder_api = get_tencent_unified_order_api()

    # prepare the data for the Tencent API
    body = '物掌柜智慧便利'
    nonce_str = str(random.random() * 10)
    ip = str(get_host_ip())
    total_fee = str(int(fee * 100))

    # sign for the data user MD5
    stringA = "appid=" + appid + "&body=" + body + "&mch_id=" + mch_id + "&nonce_str=" + nonce_str + "&notify_url=" \
            + notify_url + "&out_trade_no=" + out_trade_no + "&spbill_create_ip=" + ip + "&sub_appid=" + sub_appid \
            + "&sub_mch_id=" + sub_mchid + "&sub_openid=" + openid + "&total_fee=" + fee + "&trade_type=JSAPI"
    stringSignTemp = stringA + "&key=" + api_key
    paysign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()

    # generate the xml
    orderquery = {
        'appid': appid,
        'mch_id': mch_id,
        'sub_mch_id': sub_mchid,
        'sub_appid': sub_appid,
        'sub_openid': openid,
        'body': body,
        'nonce_str': nonce_str,
        'notify_url': notify_url,
        'out_trade_no': out_trade_no,
        'spbill_create_ip': ip,
        'total_fee': fee,
        'trade_type': 'JSAPI',
        'sign': paysign,
    }
    xml = trans_dict_to_xml(orderquery)

    error = 0
    while error < 3:
        try:
            resp = requests.post(tencent_unifiedorder_api, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
            break
        except:
            error += 1
    if error == 3:
        return 400

    # get the data for wx.payment
    msg = resp.text.encode('ISO-8859-1').decode('utf-8')
    res = trans_xml_to_dict(msg)
    print(res)
    if res.get('return_code') == 'SUCCESS':
        timestamp = round(time.time())
        timestamp = str(timestamp)
        psign = res.get('sign')
        prepay_id = res.get('prepay_id')
        package = "prepay_id=" + prepay_id
        stringB = "appId=" + sub_appid + "&nonceStr=" \
                  + nonce_str + "&package=" + package \
                  + "&signType=MD5&timeStamp=" + timestamp
        stringBSignTemp = stringB + "&key=" + api_key
        paysign = hashlib.md5(stringBSignTemp.encode('utf-8')).hexdigest().upper()
        toWxApp = {
            'timeStamp': timestamp,
            'nonceStr': nonce_str,
            'package': package,
            'signType': 'MD5',
            'paySign': paysign,
            'tradeNo': out_trade_no,
            'status': 1
        }
    else:
        toWxApp = {'return_msg': res.get('return_msg')}

    return toWxApp

def MiniAppOrderQuery(out_trade_no):
    # static data need to be put in setting
    appid = get_wechat_app_id()
    sub_appid = get_wechat_sub_app_id()
    sub_mchid = get_wechat_sub_mch_id()
    mch_id = get_wechat_mch_id()
    tencent_orderquery_api = 'https://api.mch.weixin.qq.com/pay/orderquery'

    # prepare the data for the Tencent API
    nonce_str = str(random.random()*10)

    # sign for the data user MD5
    stringA = "appid=" + appid + "&mch_id=" + mch_id + "&nonce_str=" + nonce_str + "&out_trade_no=" \
              + out_trade_no + '&sub_appid=' + sub_appid + "&sub_mch_id=" + sub_mchid
    stringSignTemp = stringA + "&key=" + get_service_api_key()
    paysign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()

    # generate the xml
    orderquery = {
        'appid': appid,
        'mch_id': mch_id,
        'sub_mch_id': sub_mchid,
        'sub_appid': sub_appid,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no,
        'sign': paysign,
    }
    xml = trans_dict_to_xml(orderquery)

    # request for tencent order query api
    error = 0
    while error < 3:
        try:
            resp = requests.post(tencent_orderquery_api, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
            break
        except:
            error += 1
    if error==3:
        resdata = {'status': 400}
        return resdata

    # get the response data
    msg = resp.text.encode('ISO-8859-1').decode('utf-8')
    xmlresp = trans_xml_to_dict(msg)

    if xmlresp.get('return_code') == 'SUCCESS':
        if xmlresp.get('result_code') == 'SUCCESS':
            resdata = {
                'status': 200,
                'trade_state': xmlresp.get('trade_state'),
                'transaction_id': xmlresp.get('transaction_id'),
                'out_trade_no': xmlresp.get('out_trade_no'),
                'cash_fee': xmlresp.get('cash_fee'),
            }
        else:
            resdata = {
                'status': 100,
                'err_code': xmlresp.get('err_code'),
                'err_code_des': xmlresp.get('err_code_des'),
            }
    else:
        resdata = {
            'status': 101,
            'return_code': xmlresp.get('return_code'),
            'return_msg': xmlresp.get('return_msg'),
        }

    return resdata



def createWechatPayQRcode(fee, out_trade_no, openid):
    # static data need to be put in setting
    appid = get_wechat_app_id()
    sub_appid = get_wechat_sub_app_id()
    sub_mchid = get_wechat_sub_mch_id()
    mch_id = get_wechat_mch_id()
    api_key = get_service_api_key()
    notify_url = get_notify_url()
    tencent_unifiedorder_api = get_tencent_unified_order_api()

    # prepare the data for the Tencent API
    body = '物掌柜智慧便利'
    nonce_str = str(random.random() * 10)
    ip = str(get_host_ip())
    fee = str(int(fee * 100))

    # sign for the data user MD5
    stringA = "appid=" + appid + "&body=" + body + "&mch_id=" + mch_id + "&nonce_str=" + nonce_str + "&notify_url=" \
              + notify_url + "&out_trade_no=" + out_trade_no + "&spbill_create_ip=" + ip + "&sub_appid=" + sub_appid \
              + "&sub_mch_id=" + sub_mchid + "&sub_openid=" + openid + "&total_fee=" + fee + "&trade_type=NATIVE"
    stringSignTemp = stringA + "&key=" + api_key
    paysign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()

    # generate the xml
    orderquery = {
        'appid': appid,
        'mch_id': mch_id,
        'sub_mch_id': sub_mchid,
        'sub_appid': sub_appid,
        'sub_openid': openid,
        'body': body,
        'nonce_str': nonce_str,
        'notify_url': notify_url,
        'out_trade_no': out_trade_no,
        'spbill_create_ip': ip,
        'total_fee': fee,
        'trade_type': 'NATIVE',
        'sign': paysign,
    }
    xml = trans_dict_to_xml(orderquery)

    error = 0
    while error < 3:
        try:
            resp = requests.post(tencent_unifiedorder_api, data=xml.encode('utf-8'),
                                 headers={'Content-Type': 'text/xml'})
            break
        except:
            error += 1
    if error == 3:
        return 'ERROR'

    # get the data for wx.payment
    msg = resp.text.encode('ISO-8859-1').decode('utf-8')
    res = trans_xml_to_dict(msg)

    if res.get('return_code') == 'SUCCESS':
        if res.get('result_code') == 'SUCCESS':
            wechatQRcode = res.get('code_url')
            return wechatQRcode
        else:
            return 'ERROR'
    else:
        return 'ERROR'


def PayOrderOnline(tradeNo, openID):
    """
    :param orderID:
    :param openID:
    :return:
    SUCCESS
    {
        'timeStamp': timestamp,
        'nonceStr': nonce_str,
        'package': package,
        'signType': 'MD5',
        'paySign': paysign,
        'tradeNo': out_trade_no,
        'status': 1
    }

    FAILED
    {
        'status' : 404
    }
    """
    order = Order.objects.get(tradeNo=tradeNo)
    payData = PayOrderByWechat(order.payPrice, order.tradeNo, openID)
    if payData == 400:
        payData = {'status': 404}
        return payData

    payData['status'] = 1  # 1 mean need a payment
    return payData


def PayOrderOffline(tradeNo, openID):
    """
        :param orderID:
        :param openID:
        :return:
        SUCCESS
        {
            'AliPayQRcodeUrl':
            'WechatPayQRcodeUrl':
            'status': 1,
        }
    """
    order = Order.objects.get(tradeNo=tradeNo)
    fee = float('%.2f' % order.payPrice)

    # generate the QRcode for Alipay and Wechat pay
    # aliQRUrl = createAlipayQRcode(fee, tradeNo)
    wechatQRUrl = createWechatPayQRcode(fee, tradeNo, openID)

    res = {
        #'AliPayQRcodeUrl': aliQRUrl,
        'WechatPayQRcodeUrl': wechatQRUrl,
        'status': 1,
    }

    return res


def PayOrderWithBalance(tradeNo):
    """
    :param orderID:
    :return:
    {
        'status' : 2,
        'balance': 'userBalance',
    }
    """
    res = {'status': 2}

    # get the data from database
    order = Order.objects.get(tradeNo=tradeNo)
    wuser = order.userID

    # edit the database of order and customer
    order.status = 1
    order.payTime = timezone.now()
    order.paymentMethod = 'Balance'
    wuser.balance = wuser.balance - order.totalPrice

    # save database
    order.save()
    wuser.save()
    serializer = DetailResponseSerializer(wuser)
    res['balance'] = serializer.data.get('balance')

    return res
