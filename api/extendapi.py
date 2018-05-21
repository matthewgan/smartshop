from aip import AipFace
import requests
import hashlib
import datetime
import random
import socket
import urllib
from xml.etree import ElementTree as et
import ssl
from bs4 import BeautifulSoup
import time

def createapiface():

    APP_ID = '11211624'
    API_KEY = 'wo7nEAvyNrK30kWG38rTC1qg'
    SECRET_KEY = 'VcHeSeIARmfXI0TahrgtMyszMsljIKnB'

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    return client


def detectface(image, imagetype, client):

    options = {}
    options['face_field'] = 'quality'
    res = client.detect(image, imagetype, options)

    errorcode = res.get('error_code')
    if errorcode == 0:
        facelist = res.get('result').get('face_list')
        quality = facelist[0].get('quality')
        angle = facelist[0].get('angle')
        yaw = angle.get('yaw')
        pitch = angle.get('pitch')
        roll = angle.get('roll')
        occlusion = quality.get('occlusion')
        blur = quality.get('blur')
        illumination = quality.get('illumination')
        completeness = quality.get('completeness')
        if float(occlusion.get('left_eye')) > 0.4 or float(occlusion.get('right_eye')) > 0.4 or float(
                occlusion.get('nose')) > 0.5 or float(occlusion.get('mouth')) > 0.5 or float(
            occlusion.get('left_cheek')) > 0.6 or float(occlusion.get('left_cheek')) > 0.6 or float(
            occlusion.get('right_cheek')) > 0.6 or float(occlusion.get('chin_contour')) > 0.4:
            print("occlusion error")
            return 100
        if float(blur) > 0.5:
            print("blur error")
            return 101
        if float(illumination) < 80:
            print("illumination error")
            return 102
        if float(completeness) < 0.3:
            print("completeness error")
            return 103
        if float(yaw) > 20 or float(yaw) < -20 or float(pitch) > 20 or float(pitch) < -20 or float(roll) > 20 or float(roll) < -20:
            return 105
    elif errorcode == 222202:
        print("no face")
        return 104

    return 200


def registerface(image, imagetype, userid, groupid, client):

    options = {}
    options["quality_control"] = "NORMAL"
    options["liveness_control"] = "LOW"
    res = client.addUser(image, imagetype, groupid, userid, options)

    return res


def searchface(image, imagetype, client):

    options= {}
    options["group_id_list"] = "customer"
    res = client.search(image,imagetype,options)
    errorcode = res.get('error_code')
    if errorcode == 0:
        userlist = res.get('result').get('user_list')
        userid = userlist.get('user_id')
        score = userlist.get('score')
        res = {}
        if float(score) > 80:
            res['status'] = 200
            res['userid'] = userid
        else:
            res['status'] = 100
            res['userid'] = userid
            res['score'] =score
    else:
        res['status'] = 101
        res['errorcode'] = errorcode
    return res


def verifyface(image, imagetype, client):

    options = {}
    options['face_fields'] = 'qualities, faceliveness'
    res = client.faceverify(image, imagetype, options)

    return res

    # errorcode = res.get('error_code')
    # if errorcode == 0:
    #     facelist = res.get('result').get('face_list')
    #     quality = facelist[0].get('quality')
    #     occlusion = quality.get('occlusion')
    #     blur = quality.get('blur')
    #     illumination = quality.get('illumination')
    #     completeness = quality.get('completeness')
    #     if float(occlusion.get('left_eye')) > 0.4 or float(occlusion.get('right_eye')) > 0.4 or float(
    #             occlusion.get('nose')) > 0.5 or float(occlusion.get('mouth')) > 0.5 or float(
    #         occlusion.get('left_cheek')) > 0.6 or float(occlusion.get('left_cheek')) > 0.6 or float(
    #         occlusion.get('right_cheek')) > 0.6 or float(occlusion.get('chin_contour')) > 0.4:
    #         print("occlusion error")
    #         return 100
    #     if float(blur) > 0.5:
    #         print("blur error")
    #         return 101
    #     if float(illumination) < 80:
    #         print("illumination error")
    #         return 102
    #     if float(completeness) < 0.3:
    #         print("completeness error")
    #         return 103
    # elif errorcode == 222202:
    #     print("no face")
    #     return 104

    return 200


def PayOrderByWechat(fee, out_trade_no, openid):
    appid = 'wx0c5669e2d0dca700'
    body = '物掌柜智慧便利'
    mch_id = '1484492962'
    nonce_str = str(random.random()*10)
    notify_url = 'https://roxaswang.mynatapp.cc/api/tencent/payNotify/'
    ip = str(get_host_ip())
    fee = str(int(fee*100))
    stringA = "appid=" + appid + "&body=" + body + "&mch_id=" + mch_id + "&nonce_str=" + nonce_str + "&notify_url=" + notify_url + "&openid=" + openid + "&out_trade_no=" + out_trade_no + "&spbill_create_ip=" + ip + "&total_fee=" + fee + "&trade_type=JSAPI"
    stringSignTemp = stringA + "&key=1E5EC81A165B729FB4DC68C6E9E286ED"
    paysign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()
    pay_xml = "<xml><appid>" + appid + "</appid><body>" + body + "</body><mch_id>" + mch_id + "</mch_id><nonce_str>" + nonce_str + "</nonce_str><notify_url>" + notify_url + "</notify_url><openid>" + openid + "</openid><out_trade_no>" + out_trade_no + "</out_trade_no><spbill_create_ip>" + ip + "</spbill_create_ip><total_fee>" + fee + "</total_fee><trade_type>JSAPI</trade_type><sign>" + paysign + "</sign></xml> "

    req = urllib.request.Request("https://api.mch.weixin.qq.com/pay/unifiedorder")
    req.add_header('User-Agent',
                   'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    ssl._create_default_https_context = ssl._create_unverified_context
    unifiedorderXML = urllib.request.urlopen(req, data=pay_xml.encode('utf-8'))

    res = trans_xml_to_dict(unifiedorderXML)

    timestamp = str(time.time())
    timestamp = timestamp[0:10]
    psign = res.get('sign')
    prepay_id = res.get('prepay_id')
    package = "prepay_id=" + prepay_id
    stringB = "appId=wx0c5669e2d0dca700&nonceStr="+nonce_str+"&package=" + package + "&signType=MD5&timeStamp=" + timestamp
    stringBSignTemp = stringB + "&key=1E5EC81A165B729FB4DC68C6E9E286ED"
    paysign = hashlib.md5(stringBSignTemp.encode('utf-8')).hexdigest().upper()

    toWxApp = {'timeStamp': timestamp, 'nonceStr': nonce_str, 'package': package, 'signType': 'MD5', 'paySign': paysign, 'tradeNo':out_trade_no, 'status': 1}

    return toWxApp


def OrderQuery(out_trade_no):
    appid = 'wx0c5669e2d0dca700'
    mch_id = '1484492962'
    nonce_str = str(random.random()*10)
    stringA = "appid=" + appid +"&mch_id=" + mch_id + "&nonce_str=" + nonce_str + "&out_trade_no=" + out_trade_no
    stringSignTemp = stringA + "&key=1E5EC81A165B729FB4DC68C6E9E286ED"
    paysign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()


    orderquery = {
        'appid': appid,
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no,
        'sign': paysign,

    }
    xml = trans_dict_to_xml(orderquery)
    print(xml)

    resp = requests.post("https://api.mch.weixin.qq.com/pay/orderquery", data=xml.encode('utf-8'),
                         headers={'Content-Type': 'text/xml'})
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

    print(resdata)

    return resdata


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