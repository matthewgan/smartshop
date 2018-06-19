# Stdlib imports
# Core Django imports
# Third-party app imports
from alipay import AliPay, ISVAliPay
# Imports from your apps


def get_app_private_key_string():
    app_private_key_string = """
        -----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2tnob+mj/sanq62Zum+ZW6gBTQCecvc0UVIpLb1mDYOeruoA
qoWOlT9tojF8z5iwIh5McmDYOXWUw8njGsx49pbBiPAIVD419SYO4pPd2C3LfoQP
KD5cAjFcJ1/9sIYzjueMguFlYL0X/1D5nngsLcfVygWPmAW3ytzZ1/C1UlqDQvnt
oRmkhcVKGdnpRc5gafFGfeCL/zgED08WX8dXG3HKz5ffEidfAoW5ZHyLVz3RPOx3
4gejyeXhivt4Yoc6A1G+0v0O+zbEDkDb6iUKJSvJfd0wu892g+JAfjdQ/n9pfmqV
v9MvERZYsjGv3hQe10+Z8ABcF0x2WoMywjXD+QIDAQABAoIBAF4/H0EqrcwnQsfF
EAHg03tMQ5sknBfIa4hlyIQBH3TMbMbI0RaeQ4P0d8M0apqAF8HpqGRNXnCIOVOD
msDMs38F9zyAmiWlUNlM1XYv1YamWg8W0ewzxq3PEe+HABpIAOYWw0UNyfm6FR6H
gagD+oqQl3nToT4HoFnFeC7tYzieI9L8ILUzbGyyiM9bUw/rATfiA256MqL4I3J6
EfWw3mF2lPZLDHXsTR6Iv5H2AbGMHB+ppoQBjOx+bnApz9GGNidYwkPmD8iLPz30
p/89Sgob2tJrzCoKA6YQon6GkOceDXl9O4jMqZ+zBN1s0sZ+FKbtgP7l2HPCXcjZ
5kVh6oECgYEA+1R3CmSapTI13aDegpYI75rKSzkArw1quyoXZ4tDaEdJEzZhAE1n
2UtJzQ0YuGV41kPHNmRF4WH/+jFBaib2irbzh5Qm++yCGRCmEw6aZYSFIxyfBsfF
Juts/lPp46XICU917V+DNlku7q8KrT5W7qDRr0CbRykIP/13aoZEUzECgYEA3ury
bDfAPua46HpcC3PAGMn4iYA8ZoRd8GyQhpFd/WlKFYjxCanrXoqP/3AJ5FiM5lSf
7y2y8p2jY7ZaiHltL28QXcDZ+koG/FfZX03D50G1tTCOIlqEuxTlL05UlHiSnb/2
EpDNV350M/4l8nm1DPkzRnw19z8GF4MnkHl5+0kCgYEAz9aFqr6PdFUVXnYODAdu
1FY5PAOjoR+DR8wDFsl/sNhigdTSWqGoY3VzTnKqIrMnPmlGcKBzeXLFcG0TH2mh
MA0jTtchdeubmoa+D7xfydvRDbw5di31x72goKFcJbmOtsRTTT1TELqnqRJvzdxj
n2q2fCr9Pdeczu4YtqraDcECgYAx5Sq/2Da6nY/z0Td7BLyRj9uGg2KBm80e/F3Z
EP6VsxR2/4DcJeFd9uvGRACi0MMw5u4pbfQo4+nnbrCS7YLn5BcotPrVT+6CWvN3
poNb5tRSKv0VaWdeLI4j6Yd6+AXxMz9T5n9fvxkpbhB2VpGUxs6YT0MRBVVKu/uG
FfqcqQKBgFCr+MH8UT3MEAWt4hDuOWIK6eUtNBujiGr64oF0qUkxdgFN4et1+fxH
02D+XTLltN8lI/NxL1iiERGf6ePn67C5pm7Xxlz8lDDwdqK9Ds7be+GDstCxu/vG
KVLedLd5/+OBm5AuS4ThYeMgZo9pzEW92nB831DYZlPTHu1ST3bN
        -----END RSA PRIVATE KEY-----
    """
    return app_private_key_string


def get_alipay_public_key_string():
    alipay_public_key_string = """
        -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAynoFVXyeU95UuaAvSCFp
lVy1tcj5A4AOUw1WJUynu4thRZCpzLMjI4dEVJhxB5TKEBcsQuE/I064lfOeVKHf
7B7jlxpF4qiTta7JRIqa5TXy8EprWK4wu10BB75mgCxsM60KFMiquF5I4hiu5RrQ
jM2YQYPyfZtle0+HTKSmvnGNYZU78UcX/gMe12Ii04giYJvAPE58S1Gz5clUFD6p
9PAd/J8gIldTKLQQ8Q9v/L0+2ED1jTqDduSVvNVjE4HVeTK8ViiGAS1OhVTO+Ywv
QV+bgDLqx+wXWoHxyt+Lb1JHCiq2BJJQdCwl1MH5gXnfw7bTKZbmMEelRKTnWWlM
4QIDAQAB
        -----END PUBLIC KEY-----
    """
    return alipay_public_key_string


def get_alipay_app_id():
    return '2018052960273226'


def get_alipay_notify_url():
    return 'https://www.wuzhanggui.shop/api/payment/alipaynotify/'


def create_alipay_client_using_isv():
    isv_alipay = ISVAliPay(
        appid=get_alipay_app_id(),
        app_notify_url=get_alipay_notify_url(),  # 默认回调url
        app_private_key_string=get_app_private_key_string(),
        alipay_public_key_string=get_alipay_public_key_string(),  # alipay public key, do not use your public key!
        sign_type="RSA2",
        debug=False,  # False by default,
        app_auth_code=None,
        app_auth_token=None
    )
    return isv_alipay


def create_alipay_client():
    alipay = AliPay(
        appid=get_alipay_app_id(),
        app_notify_url=get_alipay_notify_url(),  # 默认回调url
        app_private_key_string=get_app_private_key_string(),
        alipay_public_key_string=get_alipay_public_key_string(),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认False
    )
    return alipay


def alipay_pre_create(subject, out_trade_no, total_amount):
    """预创建支付，生成QRCODE"""
    client = create_alipay_client_using_isv()
    result = client.api_alipay_trade_precreate(
        subject="test subject",
        out_trade_no="out_trade_no",
        total_amount=total_amount
    )
    return result


def alipay_trade_page_pay(subject, out_trade_no, total_amount, return_url):
    """PC 网站支付"""
    client = create_alipay_client_using_isv()
    result = client.api_alipay_trade_page_pay(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        return_url=return_url,
    )
    return result


def alipay_trade_wap_pay(subject, out_trade_no, total_amount):
    """手机网站支付"""
    client = create_alipay_client_using_isv()
    result = client.api_alipay_trade_wap_pay(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount,
    )
    return result


def alipay_trade_app_pay(subject, out_trade_no, total_amount):
    client = create_alipay_client_using_isv()
    result = client.api_alipay_trade_app_pay(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount
    )
    return result


def alipay_trade_refund(refund_amount, out_trade_no):
    client = create_alipay_client_using_isv()
    result = client.api_alipay_trade_refund(
        refund_amount=refund_amount,
        out_trade_no=out_trade_no,

    )
    return result