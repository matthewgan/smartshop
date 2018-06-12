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
from alipay import AliPay
# Imports from your apps
from orders.models import Order
from customers.models import Customer
from  customers.serializers import DetailResponseSerializer


# Global setting given by alipay
def get_app_private_key_string():
    return '''-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrz/OU3b2Ncte4RKEGwGyBWu1ioQVn3qH/XTBoWcmlG2PrlrXXEhaLFTaXdqK1CDa7KjETOUAZ9hA8ZhuOic380+pmU5LvmoktwmOqrxGSaRJ54oIr6NFLnrIGK+KVpbEJ5J4IvU4OWm3FKX8mSzNR9e8Ziv9MrjoK2QNTDBulbs+v4B8sQTg4KjyLNOiIEEkA0pdlks70ruv8MrrGzhwlq5iQOzl+zfPJJ9CJ33TXnS1zgfgT7S01ifUguQu2NTv25l+/YxQExoxRwW33n6NbgYICNTtMYwBqVB7pS+wSenIihBRymbFu7eQejLYw53Fd88BjnzpThvFrQ7BZunWJAgMBAAECggEAXEcpPVhHGXSH9hkuH1E0NdmfS+zN2XbSrTPg7vrieYIXjY35hlTZtMOk+X6nbvHFa4sCpp+GFSt6luYEgO70qokrCOB0N6pZaTFRlHfIyUkTulD0tx6pYqMOXJAvd05xoq2eT3VVOhJJiK578xZKrweW7rIf4pBk7jSWO4FyS8wvrEO2DZVTOPr2vkEpsT7a1yHbTROmaRJmcyszhBBZwbokoMEfRygR5uh1vTKu0nb+Vv5mvq/l5gbu0jJ9Ptt/SuHQg3EbVWiAd+f2HNx4VJE4YxZTg/d7K4BUva+cQkeZWiHEuaJKRTW/ww19L6UBLMipSfMfuyL/LR72SplV8QKBgQDyZEszx+wKQD7QK3agnL1jPAxIOPORzeZ74XmVkxFtHA8KtUdvMAynte9x49xjRKM2uLVIyGpLZ4eyumASelNrU5HSU7tZgzVoQW3x5Fu0ZdxMcBhgCD0lCj5FjijgHVBhR+Uj6JG95ES9WGgYfO0XvxyjlhP/q1stdkGa3q44vQKBgQC1dUZPsrXcLpxYw7t1nLMNZ/777cUKQBCng0J3xu16qiIY3vJsNzXF1NhKIHLh8U7GXz4SWgfXcPthWjqEwV8TXUqI4zt1P98qckoWgLRIyYuo5xd98e9Fx0q6kc4T0g03fz4qv7Kra2qEZIRA3PHqL6VFQ9thEhazZU76Rpr6vQKBgC8NjROmMYnj4s2iQkr3YkRLOc8jTxT0tVNC98kzXWSi18CqZA2PdEVyKeMf6n5SqqRKwtY4IXo1xL/LMi8kE+F3vYzouCuuLsXoPaGBRNQGGfe0ouaxcr0n+eKisAihaCMaQ77uvKvyDe37pWlrhtLfRH30+jjdWLvAgwe/Rm65AoGBAKj/oU1mxsNbUdfF69g86fHJcoxVxRan1hr9P7FoPxLoUztQoP0yak1mz04ybGyMHm7Yk2nqGbWID0d7DldH9XGGiH13DJBFvWW97cyJb97+fqj/GTz+T3dwheO/GewRzKdsRYzw3smSEDFfoGD8pf4TA9y/txjwDN5lsymbCooNAoGAEpdcjuXYWmuZ5Sc1lwMBN/qmwlHpCPjeR0aG2IcBfMYXmxPnHADaH91EiyJhTEBr4S/UHTliS3rpcBuRIEreUu+l1bk0JO3oQoTqZGCANet1avL29UBHl4E7BC9G3Ud/AUUjd9H16WmFd3Mt0PdfvKrHTfh6lFdvl5R1xyVxDLg=
-----END RSA PRIVATE KEY-----'''

def get_alipay_public_key_string():
    return '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAynoFVXyeU95UuaAvSCFplVy1tcj5A4AOUw1WJUynu4thRZCpzLMjI4dEVJhxB5TKEBcsQuE/I064lfOeVKHf7B7jlxpF4qiTta7JRIqa5TXy8EprWK4wu10BB75mgCxsM60KFMiquF5I4hiu5RrQjM2YQYPyfZtle0+HTKSmvnGNYZU78UcX/gMe12Ii04giYJvAPE58S1Gz5clUFD6p9PAd/J8gIldTKLQQ8Q9v/L0+2ED1jTqDduSVvNVjE4HVeTK8ViiGAS1OhVTO+YwvQV+bgDLqx+wXWoHxyt+Lb1JHCiq2BJJQdCwl1MH5gXnfw7bTKZbmMEelRKTnWWlM4QIDAQAB
-----END PUBLIC KEY-----'''

def get_alipay_app_id():
    return '2018052960273226'


def get_alipay_notify_url():
    return 'https://www.wuzhanggui.shop/api/payment/alipaynotify/'


def get_alipay():
    # static data need to be put in setting
    appid = get_alipay_app_id()
    app_private_key_string = get_app_private_key_string()
    alipay_public_key_string = get_alipay_public_key_string()

    alipay = AliPay(
        appid=appid,
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=False,
    )

    return alipay

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



def createAlipayQRcode(fee, out_trade_no):
    # create an order
    res = get_alipay().api_alipay_trade_precreate(
        subject="物掌柜智慧便利",
        out_trade_no=out_trade_no,
        total_amount=fee,
    )

    # get QRcode
    aliQRcode = res['qr_code']

    return aliQRcode

    # check order status
    # paid = False
    # for i in range(10):
    #     # check every 3s, and 10 times in all
    #     print("now sleep 3s")
    #     time.sleep(3)
    #     result = get_alipay().api_alipay_trade_query(out_trade_no=out_trade_no)
    #     print(result)
    #     if result.get("trade_status", "") == "TRADE_SUCCESS":
    #         paid = True
    #         break
    #     print("not paid...")

    # # order is not paid in 30s , cancel this order
    # if paid is False:
    #     alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)


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
    aliQRUrl = createAlipayQRcode(fee, tradeNo)
    wechatQRUrl = createWechatPayQRcode(fee, tradeNo, openID)

    res = {
        'AliPayQRcodeUrl': aliQRUrl,
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