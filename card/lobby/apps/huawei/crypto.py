import base64
import urllib
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_V1_5_Sign

class CryptoHelper:

    @staticmethod
    def importKey(content):
        return RSA.importKey(base64.b64decode(content))

    def sign(self, data, key):
        data = self.format_data(data)
        key = CryptoHelper.importKey(key)
        h = SHA.new(data)
        signer = PKCS1_V1_5_Sign.new(key)
        signature = signer.sign(h)
        return base64.b64encode(signature)

    def checksign(self, data, data_sign, key):
        data = self.format_data(data)
        key = CryptoHelper.importKey(key)
        data_sign = urllib.unquote(data_sign)
        binary_sign = base64.b64decode(data_sign)
        verifier = PKCS1_V1_5_Sign.new(key)
        return verifier.verify(SHA.new(data), binary_sign)
        
    def format_data(self,data):
        format_data="&".join(k + "=" + str(data[k]) for k in sorted(data.keys()))
        return format_data