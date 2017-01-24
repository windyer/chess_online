#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import httplib
except ImportError:
    import http.client as httplib
import urllib
import time
import json
import base64
import itertools
import mimetypes
import md5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
'''
定义一些系统变量
'''
P_APPKEY = "appkey"
P_TIMESTAMP = "timestamp"
P_CHARSET = "charset"
P_SIGN = "sign"
P_SIGN_TYPE = "signType"
P_SELLER_ID = "sellerId"
P_API_VERSION = "apiVersion"
HOST = "open.cootekservice.com"
PORT = 80
TIMEOUT = 30
API_VERSION = '1.1'

def params2string(params, appsecret):
    ret = ''
    keys = params.keys()
    keys.sort()
    for key in keys:
        value = params[key]
        if type(value) == unicode:
            value = value.encode('utf-8')
        if type(value) == dict:
            value = json.dumps(value, sort_keys = True)
        if type(value) == list:
            value = json.dumps(value)
        if 'sign' != key and 'signType' != key and value != None and len(str(value)) > 0:
            ret += '%s=%s&' % (str(key), str(value))
    ret += 'appsecret=%s' % str(appsecret)
    return ret

def generate_sign(params, appsecret, prvKey):
    string2signed = params2string(params, appsecret)
    sign_type = params['signType']
    if 'MD5' == sign_type:
        m = md5.new(string2signed)
        return m.hexdigest().upper()
    elif 'RSA' == sign_type:
        key = RSA.importKey(base64.b64decode(prvKey))
        signer = PKCS1_v1_5.new(key)
        h = SHA.new(string2signed)
        return base64.b64encode(signer.sign(h))

def verify_sign(params, appsecret, sign, pubKey):
    string2signed = params2string(params, appsecret)
    sign_type = params['signType']
    sign = params['sign']
    if 'MD5' == sign_type:
        m = md5.new(string2signed)
        return sign == m.hexdigest().upper()
    elif 'RSA' == sign_type:
        key = RSA.importKey(base64.b64decode(pubKey))
        verifier = PKCS1_v1_5.new(key)
        h = SHA.new(string2signed)
        return verifier.verify(h, base64.b64decode(sign))

def signature_string(appsecret, parameters):
    if hasattr(parameters, "items"):
        keys = parameters.keys()
        keys.sort()
        parameters = "%s&appsecret=%s" % ('&'.join('%s=%s' % (key, mixStr(parameters[key])) for key in keys), appsecret)
    return parameters

def signature(keys, signType, appsecret, parameters):
    if signType == "MD5":
        m = md5.new(signature_string(appsecret, parameters))
        return m.hexdigest().upper()
    elif signType == "RSA":
        return keys.sign(signature_string(appsecret, parameters))
    else:
        raise Exception("only md5 and rsa are supported")

def mixStr(pstr):
    if(isinstance(pstr, str)):
        return pstr
    elif(isinstance(pstr, unicode)):
        return pstr.encode('utf-8')
    else:
        return str(pstr)

class TouchlifeException(Exception):
    pass

