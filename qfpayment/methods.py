# Stdlib imports
# Core Django imports
# Third-party app imports
import  hashlib, requests, datetime
# Imports from your apps
from qfpayment.models import Record
from orders.models import Order


def get_qf_pay_api_url():
    return 'https://openapi-test.qfpay.com/trade/v1/payment'

def get_qf_quary_api_url():
    return 'https://openapi-test.qfpay.com/trade/v1/query'

def get_qf_cancel_api_url():
    return 'https://openapi-test.qfpay.com/trade/v1/close'

def get_qf_key():
    return '12EBB96FE0C24B4DA987424812685922'

def get_qf_code():
    return '2DAB13A0AF4D4031820149BCD58188D0'

def get_qf_mchid():
    return '8w5pdhDJkm'

def qfpay_pay_qr_code(bill, trace_no):
    """
    Qianfang pay, get Alipay and Wechatpay Qrcode url
    :param bill: total_fee
    :param trace_no: out_trade_no
    :return: return QR code URL for both alipay and wechatpay
    """
    try:
        record = Record.objects.get(out_trade_no=trace_no)
    except:
        total_amount = str(int(bill * 100))
        record = Record(txdtm=total_amount, out_trade_no=trace_no)
    record.save()

    wechat_pay_type = '800201'
    alipay_pay_type = '800101'
    wechat_res = qf_get_qrcode_url(bill, trace_no, wechat_pay_type)
    alipay_res = qf_get_qrcode_url(bill, trace_no, alipay_pay_type)
    if wechat_res['status'] == 'success':
        if alipay_res['status'] == 'success':
            res = {
                'status': 'success',
                'wechat_qrcode_url': wechat_res['qrcode_url'],
                'alipay_qrcode_url': alipay_res['qrcode_url']
            }
            return res
        else:
            res = {
                'status': ' fail',
                'error_type': 'alipay_error',
                'error_msg': alipay_res['error_meg']
            }
            return res
    else:
        res = {
            'status': ' fail',
            'error_type': 'wechat_error',
            'error_msg': alipay_res['error_meg']

        }
        return res


def qf_get_qrcode_url(bill, trace_no, pay_type):

    txamt = str(int(bill * 100))
    txcurrcd = 'CNY'
    pay_type = pay_type
    out_trade_no = trace_no+pay_type
    txdtm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    goods_name = '物掌柜智慧便利'
    key = get_qf_key()
    mchid = get_qf_mchid()

    data = {'txamt': txamt, 'txcurrcd': txcurrcd, 'pay_type': pay_type,
                   'out_trade_no': out_trade_no,
                   'txdtm': txdtm, 'goods_name': goods_name, 'mchid': mchid}
    string = 'goods_name=' + goods_name + '&mchid=' + mchid + '&out_trade_no=' + out_trade_no + '&pay_type=' + pay_type + '&txamt=' + txamt + '&txcurrcd=' + txcurrcd + '&txdtm=' + txdtm + key
    md5_string = hashlib.md5(string.encode('utf-8')).hexdigest().upper()

    response_msg = requests.post(url=get_qf_pay_api_url(),
                                 data=data,
                                 headers={'X-QF-APPCODE': get_qf_code(),
                                          'X-QF-SIGN': md5_string})
    if response_msg.json()['respcd'] == '0000':
        res = {
            'status': 'success',
            'qrcode_url': response_msg.json()['qrcode']
        }
        return res
    else:
        res = {
            'status': 'fail',
            'error_code': response_msg.json()['respcd'],
            'error_meg': response_msg.json()['respmsg']
        }
        return res


def qfpay_pay_quary(trace_no):
    """
    Qianfang pay, quary the reuslt of payment
    :param trace_no: out_trade_no
    :return:
    """
    wechat_pay_type = '800201'
    alipay_pay_type = '800101'

    wechat_data = {'out_trade_no': trace_no+wechat_pay_type, 'mchid': get_qf_mchid()}
    wechat_string = 'mchid='+get_qf_mchid()+'&out_trade_no='+trace_no+wechat_pay_type+get_qf_key()
    wechat_md5_string = hashlib.md5(wechat_string.encode('utf-8')).hexdigest().upper()

    alipay_data = {'out_trade_no':trace_no+alipay_pay_type, 'mchid': get_qf_mchid()}
    alipay_string = 'mchid='+get_qf_mchid()+'&out_trade_no='+trace_no+alipay_pay_type+get_qf_key()
    alipay_md5_string = hashlib.md5(alipay_string.encode('utf-8')).hexdigest().upper()

    wechat_response_msg = requests.post(url=get_qf_quary_api_url(),
                                 data=wechat_data,
                                 headers={'X-QF-APPCODE': get_qf_code(),
                                          'X-QF-SIGN': wechat_md5_string})

    alipay_response_msg = requests.post(url=get_qf_quary_api_url(),
                                        data=alipay_data,
                                        headers={'X-QF-APPCODE': get_qf_code(),
                                                 'X-QF-SIGN': alipay_md5_string})

    pay_status = 0
    if wechat_response_msg.json()['respcd'] == '0000':
        wechat_res = wechat_response_msg.json()['data'][0]
        if wechat_res['respcd'] == '0000':
            res = {
                'status': 'success',
                'pay_type': 'Wechat',
                'paymentSN': wechat_res['syssn']
            }
            pay_status = 1;
            record = Record.objects.get(out_trade_no=trace_no)
            record.syssn = wechat_res.get('syssn')
            record.pay_type = wechat_res.get('pay_type')
            record.trade_status = wechat_res.get('cancel')
            record.txcurrcd = wechat_res.get('txcurrcd')
            record.save()

    if alipay_response_msg.json()['respcd'] == '0000':
        if alipay_response_msg.json()['data'][0]['respcd'] == '0000':
            res = {
                'status': 'success',
                'pay_type': 'Alipay',
                'paymentSN':alipay_response_msg.json()['data'][0]['syssn']
            }
            pay_status = 1;
            record = Record.objects.get(out_trade_no=trace_no)
            record.syssn = wechat_res.get('syssn')
            record.pay_type = wechat_res.get('pay_type')
            record.trade_status = wechat_res.get('cancel')
            record.txcurrcd = wechat_res.get('txcurrcd')
            record.save()

    if pay_status == 0:
        res = {
            'status': 'fail'
        }

    return res


def qfpay_pay_cancel(trace_no, pay_method):
    """
    Qianfang pay, cancel payment
    :param trace_no: out_trade_no
    :return:
    """
    if pay_method == 'Alipay':
        pay_type = '800101'
    if pay_method == 'Wechat':
        pay_type = '800201'

    order = Order.objects.get(tradeNo=trace_no)
    txamt = str(int(order.payPrice * 100))
    txdtm = order.createTime.strftime('%Y-%m-%d %H:%M:%S')

    data = {'out_trade_no': trace_no+pay_type, 'mchid': get_qf_mchid(), 'txamt': txamt, 'txdtm':txdtm}
    string = 'mchid='+get_qf_mchid()+'&out_trade_no='+trace_no+pay_type+'&txamt='+txamt+'&txdtm='+txdtm+get_qf_key()
    md5_string = hashlib.md5(string.encode('utf-8')).hexdigest().upper()

    response_msg = requests.post(url=get_qf_cancel_api_url(),
                                 data=data,
                                 headers={'X-QF-APPCODE': get_qf_code(),
                                          'X-QF-SIGN': md5_string})

    if response_msg.json()['respcd'] == '0000' or response_msg.json()['respcd'] == '1297':
        res = {
            'status': 'success'
        }
        return res
    else:
        res = {
            'status':'fail'
        }
        return res
