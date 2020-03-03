from base64 import encodebytes
from Crypto.Hash import SHA, SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from snowland_sdk.encode_encrypt import sort_dict_to_list


def _sign_with_rsa(unsigned_string, private_key, sign_type):
    """
    通过如下方法调试签名
    方法1
        key = rsa.PrivateKey.load_pkcs1(open(self._app_private_key_string).read())
        sign = rsa.sign(unsigned_string.encode("utf8"), key, "SHA-1")
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodebytes(sign).decode("utf8").replace("\n", "")
    方法2
        key = RSA.importKey(open(self._app_private_key_string).read())
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodebytes(signature).decode("utf8").replace("\n", "")
    方法3
        echo "abc" | openssl sha1 -sign tengu.key | openssl base64

    """
    # 开始计算签名
    key = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(key)
    if sign_type == "RSA":
        signature = signer.sign(SHA.new(unsigned_string.encode()))
    else:
        signature = signer.sign(SHA256.new(unsigned_string.encode()))
    # base64 编码，转换为unicode表示并移除回车
    sign = encodebytes(signature).decode("utf8").replace("\n", "")
    return sign


def gen_sign_with_rsa(data):
    data.pop("sign", None)
    sign_type = data['sign_type']
    private = '-----BEGIN RSA PRIVATE KEY-----\n{}\n-----END RSA PRIVATE KEY-----'.format(data['private_key'])
    data.pop("private_key")
    # 排序后的字符串
    ordered_items = sort_dict_to_list(data)
    unsigned_string = "&".join("{}={}".format(k, v) for k, v in ordered_items)
    sign = _sign_with_rsa(unsigned_string, private, sign_type)
    # quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in ordered_items)
    # 获得最终的订单信息字符串
    # signed_string = quoted_string + "&sign=" + quote_plus(sign)
    return sign
