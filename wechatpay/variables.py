import socket
from bs4 import BeautifulSoup

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