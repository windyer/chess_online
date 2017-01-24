#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import httplib
except ImportError:
    import http.client as httplib
import json
import base64
import md5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import  binascii
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
        if 'sign' != key and 'signType' != key :
            ret += '%s=%s&' % (str(key), str(value))
    ret =ret[:-1]
    ret += appsecret
    return ret

def generate_sign(params, appsecret, prvKey):
    string2signed = params2string(params, appsecret)
    sign_type = params['signType']
    if 'MD5' == sign_type:
        m = md5.new(string2signed)
        return m.hexdigest()
    elif 'RSA' == sign_type:
        key = RSA.importKey(base64.b64decode(prvKey))
        signer = PKCS1_v1_5.new(key)
        h = SHA.new(string2signed)
        return base64.b64encode(signer.sign(h))

def verify_sign(params, appsecret):
    string2signed = params2string(params, appsecret)
    sign = params['sign']
    m = md5.new(string2signed)
    s= m.hexdigest()
    s =binascii.b2a_hex(s)
    return sign == s

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

