# Stdlib imports
import time
import random
# Core Django imports
from django.db import models
# Third-party app imports
import hashlib
# Imports from your apps
from .variables import get_wechat_app_id, get_wechat_mch_id, get_wechat_sub_mch_id, get_wechat_sub_app_id
from .variables import get_host_ip, get_service_api_key, get_notify_url


class Record(models.Model):
    # information send to wechat to create pre-pay order
    app_id = models.CharField(max_length=20, default=get_wechat_app_id())
    mch_id = models.CharField(max_length=12, default=get_wechat_mch_id())
    sub_mch_id = models.CharField(max_length=12, default=get_wechat_sub_mch_id())
    sub_app_id = models.CharField(max_length=20, default=get_wechat_sub_app_id())
    sub_open_id = models.CharField(max_length=30)
    body = models.CharField(max_length=200, default='物掌柜智慧便利')
    nonce_str = models.CharField(max_length=10, default=str(int(random.random()*1e10)))
    notify_url = models.CharField(max_length=200, default=get_notify_url())
    out_trade_no = models.CharField(max_length=128)
    spbill_create_ip = models.CharField(max_length=20, default=get_host_ip())
    total_fee = models.CharField(max_length=20)
    trade_type = models.CharField(max_length=10)
    sign = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # information received from wechat, need to send to wechat mini app
    prepay_sign = models.CharField(max_length=100, blank=True)
    prepay_id = models.CharField(max_length=100, blank=True)
    pay_sign = models.CharField(max_length=100, blank=True)
    # information for query this payment in wechat pay system
    query_sign = models.CharField(max_length=100, blank=True)

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
                      + "&trade_type=" + str(self.trade_type) \
                      + "&key=" + get_service_api_key()
        return sign_string

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        sign_str = self.get_str_for_sign()
        self.sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
        query_str = self.get_str_for_query()
        self.query_sign = hashlib.md5(query_str.encode('utf-8')).hexdigest().upper()
        super(Record, self).save(force_update=force_update)

    def get_str_for_pay_sign(self):
        package = "prepay_id=" + str(self.prepay_id)
        sign_str = "appId=" + str(self.sub_app_id) \
                   + "&nonceStr=" + str(self.nonce_str)\
                   + "&package=" + package \
                   + "&signType=MD5" \
                   + "&timeStamp=" + str(self.timestamp)\
                   + "&key=" + get_service_api_key()
        return sign_str

    def save_pay_sign(self):
        pay_sign_str = self.get_str_for_pay_sign()
        self.pay_sign = hashlib.md5(pay_sign_str.encode('utf-8')).hexdigest().upper()
        super(Record, self).save(force_update=True)

    def get_str_for_query(self):
        str_query = "appid=" + str(self.app_id) \
                  + "&mch_id=" + str(self.mch_id) \
                  + "&nonce_str=" + str(self.nonce_str) \
                  + "&out_trade_no=" + str(self.out_trade_no) \
                  + '&sub_appid=' + str(self.sub_app_id) \
                  + "&sub_mch_id=" + str(self.sub_mch_id) \
                  + "&key=" + get_service_api_key()
        return str_query

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
            'trade_type': self.trade_type,
            'sign': self.sign,
        }
        return model_dict

    def model_query_to_dict(self):
        query_dict = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'sub_mch_id': self.sub_mch_id,
            'sub_appid': self.sub_app_id,
            'nonce_str': self.nonce_str,
            'out_trade_no': self.out_trade_no,
            'sign': self.query_sign,
        }
        return query_dict

    def prepay_response_to_dict(self):
        package = "prepay_id=" + str(self.prepay_id)
        response_dict = {
            'status': 'success',
            'timeStamp': str(self.timestamp),
            'nonceStr': str(self.nonce_str),
            'package': package,
            'signType': 'MD5',
            'paySign': self.pay_sign,
            'tradeNo': self.out_trade_no,
        }
        return response_dict

    def __str__(self):
        return self.out_trade_no

    class Meta:
        verbose_name = "微信支付记录"
        verbose_name_plural = "微信支付记录"
