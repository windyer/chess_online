import base64

from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_V1_5_Sign

class CryptoHelper:

    @staticmethod
    def importKey(content):
        return RSA.importKey(base64.b64decode(content))

    def sign(self, data, key):
        hash = MD5.new(data)
        signature = PKCS1_V1_5_Sign.new(key)
        return base64.b64encode(signature.sign(hash))

    def checksign(self, data, data_sign, key):          
        binary_sign = base64.b64decode(data_sign)        
        verifier = PKCS1_V1_5_Sign.new(key)
        return verifier.verify(MD5.new(data), binary_sign)
        
    def segmentation_data(self, reqData, platpkey):
        data=reqData.split('&')
        tdata=data[0].split('=')
        transdata=tdata[1].replace('+',' ')
        if data[1] is None:
             return transdata
        else:
            tsign=data[1].split('=')
            sign=tsign[1]+"="
        if data[2] is None:
            return transdata
        else:
            tsigntype=data[2].split('=')
            signtype=tsigntype[1]
            i=self.checksign(transdata, sign, platpkey)
            return i
