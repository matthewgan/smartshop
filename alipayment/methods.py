# Stdlib imports
# Core Django imports
# Third-party app imports
from alipay import AliPay, ISVAliPay
# Imports from your apps
from .models import Record

def get_app_private_key_string():
    return '''-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrz/OU3b2Ncte4RKEGwGyBWu1ioQVn3qH/XTBoWcmlG2PrlrXXEhaLFTaXdqK1CDa7KjETOUAZ9hA8ZhuOic380+pmU5LvmoktwmOqrxGSaRJ54oIr6NFLnrIGK+KVpbEJ5J4IvU4OWm3FKX8mSzNR9e8Ziv9MrjoK2QNTDBulbs+v4B8sQTg4KjyLNOiIEEkA0pdlks70ruv8MrrGzhwlq5iQOzl+zfPJJ9CJ33TXnS1zgfgT7S01ifUguQu2NTv25l+/YxQExoxRwW33n6NbgYICNTtMYwBqVB7pS+wSenIihBRymbFu7eQejLYw53Fd88BjnzpThvFrQ7BZunWJAgMBAAECggEAXEcpPVhHGXSH9hkuH1E0NdmfS+zN2XbSrTPg7vrieYIXjY35hlTZtMOk+X6nbvHFa4sCpp+GFSt6luYEgO70qokrCOB0N6pZaTFRlHfIyUkTulD0tx6pYqMOXJAvd05xoq2eT3VVOhJJiK578xZKrweW7rIf4pBk7jSWO4FyS8wvrEO2DZVTOPr2vkEpsT7a1yHbTROmaRJmcyszhBBZwbokoMEfRygR5uh1vTKu0nb+Vv5mvq/l5gbu0jJ9Ptt/SuHQg3EbVWiAd+f2HNx4VJE4YxZTg/d7K4BUva+cQkeZWiHEuaJKRTW/ww19L6UBLMipSfMfuyL/LR72SplV8QKBgQDyZEszx+wKQD7QK3agnL1jPAxIOPORzeZ74XmVkxFtHA8KtUdvMAynte9x49xjRKM2uLVIyGpLZ4eyumASelNrU5HSU7tZgzVoQW3x5Fu0ZdxMcBhgCD0lCj5FjijgHVBhR+Uj6JG95ES9WGgYfO0XvxyjlhP/q1stdkGa3q44vQKBgQC1dUZPsrXcLpxYw7t1nLMNZ/777cUKQBCng0J3xu16qiIY3vJsNzXF1NhKIHLh8U7GXz4SWgfXcPthWjqEwV8TXUqI4zt1P98qckoWgLRIyYuo5xd98e9Fx0q6kc4T0g03fz4qv7Kra2qEZIRA3PHqL6VFQ9thEhazZU76Rpr6vQKBgC8NjROmMYnj4s2iQkr3YkRLOc8jTxT0tVNC98kzXWSi18CqZA2PdEVyKeMf6n5SqqRKwtY4IXo1xL/LMi8kE+F3vYzouCuuLsXoPaGBRNQGGfe0ouaxcr0n+eKisAihaCMaQ77uvKvyDe37pWlrhtLfRH30+jjdWLvAgwe/Rm65AoGBAKj/oU1mxsNbUdfF69g86fHJcoxVxRan1hr9P7FoPxLoUztQoP0yak1mz04ybGyMHm7Yk2nqGbWID0d7DldH9XGGiH13DJBFvWW97cyJb97+fqj/GTz+T3dwheO/GewRzKdsRYzw3smSEDFfoGD8pf4TA9y/txjwDN5lsymbCooNAoGAEpdcjuXYWmuZ5Sc1lwMBN/qmwlHpCPjeR0aG2IcBfMYXmxPnHADaH91EiyJhTEBr4S/UHTliS3rpcBuRIEreUu+l1bk0JO3oQoTqZGCANet1avL29UBHl4E7BC9G3Ud/AUUjd9H16WmFd3Mt0PdfvKrHTfh6lFdvl5R1xyVxDLg=
-----END RSA PRIVATE KEY-----'''


def get_alipay_public_key_string():
    return '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAynoFVXyeU95UuaAvSCFplVy1tcj5A4AOUw1WJUynu4thRZCpzLMjI4dEVJhxB5TKEBcsQuE/I064lfOeVKHf7B7jlxpF4qiTta7JRIqa5TXy8EprWK4wu10BB75mgCxsM60KFMiquF5I4hiu5RrQjM2YQYPyfZtle0+HTKSmvnGNYZU78UcX/gMe12Ii04giYJvAPE58S1Gz5clUFD6p9PAd/J8gIldTKLQQ8Q9v/L0+2ED1jTqDduSVvNVjE4HVeTK8ViiGAS1OhVTO+YwvQV+bgDLqx+wXWoHxyt+Lb1JHCiq2BJJQdCwl1MH5gXnfw7bTKZbmMEelRKTnWWlM4QIDAQAB
-----END PUBLIC KEY-----'''


# def get_app_private_key_string():
#     app_private_key_string = """
#         -----BEGIN RSA PRIVATE KEY-----
# MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCpUulzxadvBVXgAG5D5lrQct5JCkQFS+qyCfq7VOw516CwnxoX9XQF6VCN3gBzyR293BomP1gkSxRiZy3eH5F2N7ROPHvvZn8Mr2+hVfAwVIhEDogHGLIWJIbI0BpfHzo43JZL7Gn4b22sj6NFpOqxnxPBp8K+oxHW3RF/hsBJb1ngnjbs/O8ezSfmNqtcwTbbMArnkG3STs5649QuPpHItv98obD1Ew6lJ+i/7eyPcaXzMEUuJqdvPlY50O5hRjupA6EchL8G6V2o2cD3hoik7doH5+1RF8JGbK8iBJs9UMqMBw1OddwENxmFf2Ky5AqHrl3xknCUq6nWlLrnhigrAgMBAAECggEAApYSnMMTGJ4DPsWi6YSWNILcpE701QPg1NFUNBJK/WMuwCPd+Sm1mPWEVnZimWIkAydeeuESzpMa/5nF2JOw3BZjuaIw3mo5XI89bEBsx8AyyJ9UMo+NAMuUB3MuQ++tKvsrjINS5wmEqlMTUlf/gbEFUzrlvZWuCxMbVlBPlY+IdC8w5ktsT7HfvyAPxTJ0L2DR6zG3xDk3BFM2p7rH+UfjXQcR5hSA1R5bAbGrlpdMd0Fl3NXoQPRIq/ebqQZlzzS2tNdvFDMV6HNRwRbfH53Cg/vFoE9qVqjFJGCV7qMFDSJ1vcPaQaJWJeS5x2DsPlU8MoWjFrUVmexmEtpj8QKBgQDjtNnabgiJNM6j0pYUFjI4X02mbY49BgRe7kZF7cDsAMN7mcScriZKvuSp1Z4K999/SxFLnca6C3SRH1uZujMM+Ph7I8cK5IwIL9bqbavR5SubJbu4pejjbHCWFgT68m5py6eAg+XiTwemen/Dlyg4TRMhCLIQ3Ri7cD4MMfnYgwKBgQC+XPX0SKeFFa3X9gKRU8zJVQKKUreF+dFoQBbIk38Aje6/PYq/llvH1RRpnKX+rhr1qvgST7rzDTWIrvlj1dx+1kV6/hNl+GFl9YAZsdidDMSDfRSFdn031NeTxDQ69f1Pk741A3EGXtkQRFFJqb9/juEtHZokzs1q8fmXoLbROQKBgBlhijrvsuHgUfwut+3LP5PLA7O+WHFy3z/ZnVmkE7H6r89yJ1kzjC8esgxANFqSoIXmzym3j3QjXL3kWeh7ub8DbWcEaOZM7VLoSjNdQB6oRcEIZrFBRQE8kBwanjl+llISkjwf95rPJlInK2CY07Ha3Xv8JST+EAisjS380BWTAoGAO1zX4i7J9ql1BdSUpmcghGQ7H5F944ys7bqWoEPGphCctAxn+SjVRDLBY9HSveHjTFrdczBj1yl2WUJfSO/HC9Kb5ifXOsRC8z2kjd608vypR2u4+4mgsMlx1IWp1/0f2jHzbaq+E0N+oyD6zGLf8dJHi/8gM3w9+KyurccTW5kCgYBKHMA4ypraT82j611TVGO8tIfpiJscHe5iILrlzU0aNx4svXkN+X64UfW/9WjTdj2Qz5+OGj2hn/fnJLB0ONr8jOQc/Wau1eMcy/ewcGbs8Cqn/23EKEiTLOig8W8HLhafoIVyi2OlWR+/UzlQhYqRcorPFgobpk33/x7dQlSrBg==
#         -----END RSA PRIVATE KEY-----
#     """
#     return app_private_key_string
#
#
# def get_alipay_public_key_string():
#     alipay_public_key_string = """
#         -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqVLpc8WnbwVV4ABuQ+Za0HLeSQpEBUvqsgn6u1TsOdegsJ8aF/V0BelQjd4Ac8kdvdwaJj9YJEsUYmct3h+Rdje0Tjx772Z/DK9voVXwMFSIRA6IBxiyFiSGyNAaXx86ONyWS+xp+G9trI+jRaTqsZ8TwafCvqMR1t0Rf4bASW9Z4J427PzvHs0n5jarXME22zAK55Bt0k7OeuPULj6RyLb/fKGw9RMOpSfov+3sj3Gl8zBFLianbz5WOdDuYUY7qQOhHIS/BuldqNnA94aIpO3aB+ftURfCRmyvIgSbPVDKjAcNTnXcBDcZhX9isuQKh65d8ZJwlKup1pS654YoKwIDAQAB
#         -----END PUBLIC KEY-----
#     """
#     return alipay_public_key_string


def get_alipay_app_id():
    return '2018052960273226'


def get_alipay_notify_url():
    return 'https://www.wuzhanggui.shop/api/payment/alipaynotify/'


def create_alipay_client_using_isv():
    isv_alipay = ISVAliPay(
        appid=get_alipay_app_id(),
        app_notify_url=get_alipay_notify_url(),  # 默认回调url
        app_private_key_string=get_app_private_key_string(),
        alipay_public_key_string=get_alipay_public_key_string(),  # alipayment public key, do not use your public key!
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
    # client = create_alipay_client_using_isv()
    client = create_alipay_client()
    result = client.api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount,
    )
    print('Alipay Response:')
    print(result)
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


def alipay_trade_query(out_trade_no):
    client = create_alipay_client()
    result = client.api_alipay_trade_query(out_trade_no=out_trade_no)
    print(result)
    if result.get("trade_status") == "TRADE_SUCCESS":
        resp_data = {
            'status': 200,
            'trade_state': result.get('trade_status'),
            'trade_no': result.get('trade_no'),
            'out_trade_no': result.get('out_trade_no'),
            'cash_fee': result.get('total_amount'),
        }

        record = Record.objects.get(out_trade_no=out_trade_no)
        record.trade_no = result.get('trade_no')
        record.buyer_user_id = result.get('buyer_user_id')
        record.buyer_logon_id = result.get('buyer_logon_id')
        record.trade_status = result.get('trade_status')
        record.invoice_amount = result.get('invoice_amount')
        record.receipt_amount = result.get('receipt_amount')
        record.save()

    else:
        resp_data = {
            'status': 100,
            'msg': result.get('msg'),
            'sub_code': result.get('sub_code'),
            'sub_msg': result.get('sub_msg'),
        }
    return resp_data


def alipay_trade_cancel(out_trade_no):
    client = create_alipay_client()
    result = client.api_alipay_trade_cancel(out_trade_no=out_trade_no)
    if result.get('code') == '10000':
        resp_data = {
            'status': 200,
            'trade_no': result.get('trade_no'),
        }
    else:
        resp_data = {
            'status': 100,
            'msg': result.get('msg'),
            'sub_code': result.get('sub_code'),
            'sub_msg': result.get('sub_msg'),
        }
    return resp_data


def alipay_qr_code(out_trade_no, total_amount):
    subject = '物掌柜智慧便利'
    response = alipay_pre_create(subject=subject, out_trade_no=out_trade_no, total_amount=total_amount)
    if response.get('code') == "10000":
        qr_code = response.get('qr_code')
        out_trade_no = response.get('out_trade_no')
        try:
            record = Record.objects.get(out_trade_no=out_trade_no)
        except:
            record = Record(out_trade_no=out_trade_no, total_amount=total_amount, operation='PRECREATE', qr_code=qr_code)
        record.save()
        return response.get('qr_code')
    else:
        # TODO
        return None