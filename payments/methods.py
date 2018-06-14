"""
Useful functions and methods related to payment
"""
# Stdlib imports
import datetime
import socket
# Core Django imports
# Third-party app imports
from bs4 import BeautifulSoup
import requests
# Imports from your apps


"""
Global variables given by wechat pay
"""
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


def get_tencent_unified_order_api():
    return 'https://api.mch.weixin.qq.com/pay/unifiedorder'


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


def get_host_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        return ip
    finally:
        sock.close()


def iso_format(time):
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
