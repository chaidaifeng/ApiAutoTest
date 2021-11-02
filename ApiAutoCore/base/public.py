# -*- coding: utf-8 -*-
"""
@File:public.py
@Author:cdf
@Version:1.0
@Description:公共方法封装
"""

import os
from pyDes import des, CBC, PAD_PKCS5
import base64
from urllib.parse import quote, unquote


# 指定目录拼接文件名路径
def filePath(*filename):

    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), *filename)


# URL加密
def url_quote(s):
    s_quote = quote(s)
    return s_quote


# URL解密
def url_unquote(s):
    s_unquote = unquote(s)
    return s_unquote


# 密码加密
def des_encrypt(s=None, secret_key=None, iv=None):
    if iv is None and secret_key is not None:
        iv = secret_key
    # secret_key:加密密钥，CBC:加密模式，iv:偏移, pad_mode:填充
    des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    # 返回为字节
    secret_bytes = des_obj.encrypt(s)
    # 返回为16进制
    return base64.b64encode(secret_bytes).decode()


# 密码解密
def des_crypt(s=None, secret_key=None, iv=None):
    if iv is None and secret_key is not None:
        iv = secret_key
    des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    decrypt_str = des_obj.decrypt(base64.b64decode(s))
    return decrypt_str.decode()


if __name__ == '__main__':
    s1 = "李诺"
    url = 'https://www.pinpin.com/api/resume/search/list.json?keyword={}&current=1&pageSize=30&company=1'.format(url_quote(s1))
    # print(url)
    # print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    # print(filePath('data1', 'data2', 'data3'))
    # print(des_encrypt("sss"))
    print(des_encrypt('test123', 'RUYUKEY1', 'RUYUKEY2'))
    print(des_crypt('ajFLisVReGs=', 'RUYUKEY1', 'RUYUKEY2'))
