# Stdlib imports
# Core Django imports
# Third-party app imports
import requests
# Imports from your apps
from .models import Record
from retry.methods import retry_on_500, retry_on_auth_failure, retry_on_server_error
from .variables import trans_xml_to_dict, trans_dict_to_xml
from .variables import get_tencent_unified_order_api


@retry_on_500
def request_post_with_retry(url, data, headers):
    return requests.post(url=url, data=data, headers=headers)


def wechat_pay(bill, trace_no, open_id):
    """
    Online wechat pay, with default trade type JSAPI
    :param bill: total_fee
    :param trace_no: out_trade_no
    :param open_id: user_wechat_id
    :return: return message from wechat
    """
    try:
        record = Record.objects.get(out_trade_no=trace_no)
    except:
        total_amount = str(int(bill * 100))
        record = Record(total_fee=total_amount, out_trade_no=trace_no, sub_open_id=open_id, trade_type='JSAPI')

    record.save()
    model_dict = record.model_to_dict()
    model_xml = trans_dict_to_xml(model_dict)
    # send to wechat with retry
    response_msg = requests.post(url=get_tencent_unified_order_api(),
                                           data=model_xml.encode('utf-8'),
                                           headers={'Content-Type': 'text/xml'})
    # get the data for wx.payment
    response_msg = response_msg.text.encode('ISO-8859-1').decode('utf-8')
    res = trans_xml_to_dict(response_msg)
    if res.get('return_code') == 'SUCCESS':
        record.prepay_sign = res.get('sign')
        record.prepay_id = res.get('prepay_id')
        record.save_pay_sign()
        return record.prepay_response_to_dict()
    else:
        return {
            'status': 'fail',
            'error_msg': res.get('return_msg'),
        }


def wechat_pay_query(trace_no):
    # static data need to be put in setting
    tencent_order_query_api = 'https://api.mch.weixin.qq.com/pay/orderquery'
    record = Record.objects.get(out_trade_no=trace_no)
    query_dict = record.model_query_to_dict()
    query_xml = trans_dict_to_xml(query_dict)
    response_msg = requests.post(url=tencent_order_query_api,
                                           data=query_xml.encode('utf-8'),
                                           headers={'Content-Type': 'text/xml'})
    # get the response data
    msg = response_msg.text.encode('ISO-8859-1').decode('utf-8')
    resp_xml = trans_xml_to_dict(msg)
    print('Wechat Pay Response: ')
    print(resp_xml)
    if resp_xml.get('return_code') == 'SUCCESS':
        if resp_xml.get('trade_state') == 'SUCCESS':
            resp_data = {
                'status': 200,
                'trade_state': resp_xml.get('trade_state'),
                'transaction_id': resp_xml.get('transaction_id'),
                'out_trade_no': resp_xml.get('out_trade_no'),
                'cash_fee': resp_xml.get('cash_fee'),
            }
        else:
            resp_data = {
                'status': 100,
                'trade_state': resp_xml.get('trade_state'),
            }
    else:
        resp_data = {
            'status': 101,
            'return_code': resp_xml.get('return_code'),
            'return_msg': resp_xml.get('return_msg'),
        }
    return resp_data


def wechat_pay_qr_code(bill, trace_no, open_id):
    """
    Online wechat pay, with default trade type NATIVE
    :param bill: total_fee
    :param trace_no: out_trade_no
    :param open_id: user_wechat_id
    :return: return QR code URL from wechat
    """
    try:
        record = Record.objects.get(out_trade_no=trace_no)
    except:
        total_amount = str(int(bill * 100))
        record = Record(total_fee=total_amount, out_trade_no=trace_no, sub_open_id=open_id, trade_type='NATIVE')
    record.save()
    model_dict = record.model_to_dict()
    model_xml = trans_dict_to_xml(model_dict)
    # send to wechat with retry
    response_msg = requests.post(url=get_tencent_unified_order_api(),
                                 data=model_xml.encode('utf-8'),
                                 headers={'Content-Type': 'text/xml'})
    # get the data for wx.payment
    response_msg = response_msg.text.encode('ISO-8859-1').decode('utf-8')

    res = trans_xml_to_dict(response_msg)
    print('Wechat Pay Response: ')
    print(res)
    if res.get('return_code') == 'SUCCESS':
        if res.get('result_code') == 'SUCCESS':
            code_url = res.get('code_url')
            return code_url
        else:
            return 'ERROR'
    else:
        return 'ERROR'


def wechat_pay_cancel(trace_no):
    """
    Cancel wechat pay order
    :param trace_no: out_trade_no
    :return: return QR code URL from wechat
    """
    # static data need to be put in setting
    tencent_order_cancel_api = 'https://api.mch.weixin.qq.com/pay/closeorder'
    record = Record.objects.get(out_trade_no=trace_no)
    query_dict = record.model_query_to_dict()
    query_xml = trans_dict_to_xml(query_dict)
    response_msg = requests.post(url=tencent_order_cancel_api,
                                           data=query_xml.encode('utf-8'),
                                           headers={'Content-Type': 'text/xml'})
    # get the response data
    msg = response_msg.text.encode('ISO-8859-1').decode('utf-8')
    resp_xml = trans_xml_to_dict(msg)

    if resp_xml.get('return_code') == 'SUCCESS':
        if resp_xml.get('result_code') == 'SUCCESS':
            resp_data = {
                'status': 200,
            }
        else:
            resp_data = {
                'status': 100,
                'err_code': resp_xml.get('err_code'),
                'err_code_des': resp_xml.get('err_code_des'),
            }
    else:
        resp_data = {
            'status': 101,
            'return_code': resp_xml.get('return_code'),
            'return_msg': resp_xml.get('return_msg'),
        }
    return resp_data