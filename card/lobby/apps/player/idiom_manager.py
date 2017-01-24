__all__ = ['IdiomManager']

import random
import time
import urllib
import base64
import ujson
from Crypto.Cipher import AES

from card.core.conf import settings
from card.lobby.settings.coder_conversion import CODE_CONVERSION


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * " "
#pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
#unpad = lambda s : s[0:-ord(s[-1])]


class IdiomManager(object):

    def random_idiom(self):
        idioms = CODE_CONVERSION.idiom_table
        key = random.choice(idioms.keys())
        idiom = idioms[key]
        key_dict = {}
        key_dict["key"] = key
        key_dict["timestamp"] = int(time.time())
        json_dict = ujson.dumps(key_dict)

        aes_key = settings.PLAYER.idiom_aes_key
        cipher = AES.new(aes_key, AES.MODE_ECB)

        paded_json = pad(json_dict)
        encoded_key = cipher.encrypt(paded_json).strip()
        encoded_key = base64.b64encode(encoded_key)
        encoded_key = urllib.quote(encoded_key)

        return encoded_key, idiom