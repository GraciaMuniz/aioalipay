import json
from base64 import encodebytes

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


def sign_data(app_private_key, data):
    """只支持RSA2"""
    data.pop("sign", None)
    # 排序后的字符串
    unsigned_items = _ordered_data(data)
    unsigned_string = "&".join(
        "{}={}".format(k, v) for k, v in unsigned_items)
    sign = _sign(app_private_key, unsigned_string)
    return sign


def _ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据dump出来
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))

    return sorted([(k, v) for k, v in data.items()])


def _sign(app_private_key, unsigned_string):
    # 开始计算签名
    signer = PKCS1_v1_5.new(app_private_key)
    signature = signer.sign(SHA256.new(unsigned_string.encode('utf-8')))
    # base64 编码，转换为unicode表示并移除回车
    sign = encodebytes(signature).decode("utf-8").replace("\n", "")
    return sign
