# Stdlib imports
import time
import random
import socket
import datetime
import requests
# Core Django imports
from django.utils import timezone
# Third-party app imports
import hashlib
import datetime
from bs4 import BeautifulSoup
from django.http import JsonResponse
# Imports from your apps
from orders.models import Order
from customers.models import Customer
from customers.serializers import DetailResponseSerializer


# Global setting given by wechat
def get_wechat_app_id():
    return 'wxff1e7b77ac356972'


def get_wechat_sub_app_id():
    return 'wx18902f96ec8fb847'


def get_wechat_mch_id():
    return '1484700102'


def get_wechat_sub_mch_id():
    return '1505139251'


def get_service_api_key():
    return 'PRiiXyGL0ULPRiiXyGL0UL8888888888'


def get_notify_url():
    return 'https://www.wuzhanggui.shop/api/payment/wechatnotify/'


def get_tencent_unifiedorder_api():
    return 'https://api.mch.weixin.qq.com/pay/unifiedorder'


def isoformat(time):
    """
    将datetime或者timedelta对象转换成ISO 8601时间标准格式字符串
    :param time: 给定datetime或者timedelta
    :return: 根据ISO 8601时间标准格式进行输出
    """
    if isinstance(time, datetime.datetime):
        # 如果输入是datetime
        return time.isoformat()
    elif isinstance(time, datetime.timedelta):
        # 如果输入时timedelta，计算其代表的时分秒
        hours = time.seconds // 3600
        minutes = time.seconds % 3600 // 60
        seconds = time.seconds % 3600 % 60
        return 'P%sDT%sH%sM%sS' % (time.days, hours, minutes, seconds)
        # 将字符串进行连接


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def trans_xml_to_dict(xml):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象
    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """
    soup = BeautifulSoup(xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
    return data


def trans_dict_to_xml(data):
    """
    将 dict 对象转换成微信支付交互所需的 XML 格式数据
    :param data: dict 对象
    :return: xml 格式数据
    """
    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))


def PayOrderByWechat(fee, out_trade_no, openid):

    # static data need to be put in setting
    appid = get_wechat_app_id()
    sub_appid = get_wechat_sub_app_id()
    sub_mchid = get_wechat_sub_mch_id()
    mch_id = get_wechat_mch_id()
    api_key = get_service_api_key()
    notify_url = get_notify_url()
    tencent_unifiedorder_api = get_tencent_unifiedorder_api()

    # prepare the data for the Tencent API
    body = '物掌柜智慧便利'
    nonce_str = str(random.random()*10)
    ip = str(get_host_ip())
    fee = str(int(fee*100))

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
        'trade_type':'JSAPI',
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

    # request for tencent orderquery api
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
    tencent_unifiedorder_api = get_tencent_unifiedorder_api()

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
    order.payPrice = order.totalPrice
    order.balanceUse = order.payPrice
    order.paymentMethod = 'Balance'
    wuser.balance = wuser.balance - order.totalPrice

    # save database
    order.save()
    wuser.save()
    serializer = DetailResponseSerializer(wuser)
    res['balance'] = serializer.data.get('balance')

    return res