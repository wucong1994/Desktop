import hashlib
import html
import json
import urllib
import base64

import requests
from django.db.models import ManyToManyField, DateField, TimeField, DateTimeField



class toDictRoot:
    '''
    model转字典基类
    '''
    def toDICT(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None

            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S.%f') if value else None
            elif isinstance(f, TimeField):
                value = value.strftime('%H:%M:%S.%f') if value else None
            elif isinstance(f, DateField):
                value = value.strftime('%Y-%m-%d') if value else None

            data[f.name] = value
        return data

    def toJSON(self, fields=None, exclude=None):
        return json.dumps(self.toDICT(fields=fields, exclude=exclude), separators=(',', ':'))


def send_msg(phone, msg, url):
    '''
    发送短信
    :param phone:手机号
    :param msg:短信内容
    :param url:发送短信地址
    :return:
    '''
    try:
        msg = urlencode(msg)
        url = url.format(phone, msg)
        res = requests.get(url)
        json_response = json.loads(res.content)
        # 设置验证码
        if json_response.get('result') == 'success':
            return True
        else:
            return False
    except Exception as e:
        raise Exception


def sort_dict_to_list(data):
    '''
    将字典按字母序排序
    :param data:
    :return: 元素为(key, value)元组的列表
    '''
    if data is None or len(data)==0:
        raise ValueError

    if not isinstance(data, dict):
        raise TypeError

    complex_keys = [k for k, v in data.items() if isinstance(v, dict)]

    # 将字典类型的数据dump出来
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))

    return sorted([(k, v) for k, v in data.items()])


def md5_hexdigest(encry=None, upper=False):
    '''
    16 进制 32 位 加密
    :param encry: 要加密的字符串
    :param upper: 是要大写
    :return:
    '''
    if encry is None:
        raise ValueError

    if not isinstance(encry, str):
        raise TypeError

    m = hashlib.md5(encry.encode(encoding='utf-8'))
    if not upper:
        return m.hexdigest()
    else:
        return m.hexdigest().upper()


def md5_digest(encry=None):
    '''
    2 进制 16 位 加密
    :param encry: 要加密的字符串
    :return:
    '''
    if encry is None:
        raise ValueError

    if not isinstance(encry, str):
        raise TypeError

    m = hashlib.md5(encry.encode(encoding='utf-8'))
    return m.digest().decode().encode('utf-8')


def xor_decrypt(tips, key='9'):
    '''
    异或解密
    :param tips: 密文
    :param key: 秘钥
    :return:
    '''
    lkey = len(key)
    secret = []
    num = 0
    for each in tips:
        if num >= lkey:
            num = num % lkey
        secret.append(ord(chr(ord(each) ^ ord(key[num]))))
        num += 1
    result = ''.join([str(i) for i in secret])
    return result


def urldecode(b):
    '''
    url解码
    :param b:
    :return:
    '''
    if b is None:
        raise ValueError

    if not isinstance(b, bytes):
        raise TypeError

    data = urllib.parse.unquote(b)
    return data


def urlencode(s):
    '''
    url编码
    :param s:
    :return:
    '''
    if s is None:
        raise ValueError

    if type(s) not in [str, bytes]:
        raise TypeError
    data = urllib.parse.quote(s)
    return data


def base64encode(b):
    '''
    base64编码
    :param b:
    :return:
    '''
    if b is None:
        ValueError

    if not isinstance(b, bytes):
        raise TypeError

    return base64.b64encode(b)


def base64decode(s):
    '''
    base64 解码
    :param s:
    :return:
    '''
    if s is None:
        raise ValueError

    if type(s) not in [str, bytes]:
        raise TypeError

    s = str(base64.urlsafe_b64decode(s), encoding='utf8')
    s = html.unescape(s)  # 反转义html字符
    return s



