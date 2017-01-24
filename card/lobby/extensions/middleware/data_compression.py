__all__ = ['DataCompressionMiddleware']

import json

from card.core.conf import settings

class DataCompressionMiddleware(object):
    def __init__(self):
        super(DataCompressionMiddleware, self).__init__()
        self._encoder_dict = settings.CODE_CONVERSION.dicts['encoder']

    def _encoder_json_value(self, json_value):
        if isinstance(json_value, list):
            encoder_list = []
            for value in json_value:
                encoder_value = self._encoder_json_value(value)
                encoder_list.append(encoder_value)
            return encoder_list
        elif isinstance(json_value, dict):
            encoder_dict = {}
            for key, value in json_value.iteritems():
                if value is None:
                    continue
                if key in self._encoder_dict:
                    encoder_key = self._encoder_dict[key]
                    encoder_value = self._encoder_json_value(value)
                    encoder_dict[encoder_key] = encoder_value
                else:
                    encoder_value = self._encoder_json_value(value)
                    encoder_dict[key] = encoder_value
            return encoder_dict
        else:
            encoder_value = json_value
            return encoder_value

    def _need_encoder(self, json_content):
        if 'disable_encoder' in json_content:
            del json_content['disable_encoder']
            return False
        else:
            return True

    def _encoder(self, response):
        json_content = json.loads(response.content)

        if self._need_encoder(json_content):
            json_encoder = self._encoder_json_value(json_content)
        else:
            json_encoder = json_content

        json_resp = json.dumps(json_encoder, separators=(',',':'))
        response.content = json_resp
        return response

    def process_response(self, request, response):
        if settings.CODE_CONVERSION.need_encode:
            if response._headers['content-type'][1] == 'application/json':
                response = self._encoder(response)
            elif 'application/json' in response.get('content-type', ''):
                response = self._encoder(response)

        return response
