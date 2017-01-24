from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.compat import StringIO
from rest_framework.renderers import XMLRenderer
from rest_framework.parsers import XMLParser

import dicttoxml
import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.mobile.service import MobileService
from card.lobby.apps.mobile import serializers

class MobileXMLPaerser(XMLParser):

    XML_NS = "{http://www.monternet.com/dsmp/schemas/}"

    def _xml_convert(self, element):
        children = list(element)

        if len(children) == 0:
            return element.text
        else:
            if children[0].tag == "list-item":
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag[len(self.XML_NS):]] = self._xml_convert(child)

            return data

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'charge/notify': reverse('mobile-notify', request=request, format=format),
    })

@go.logging.class_wrapper
class ChargeNotify(generics.CreateAPIView):

    parser_classes = (MobileXMLPaerser,)
    serializer_class = serializers.ChargeNotifyRequest

    def _xml_encode(self, data, encoding, root):
        xml = '<?xml version="1.0" encoding="{0}"?>'.format(encoding)
        xml += '<{0} xmlns="http://www.monternet.com/dsmp/schemas/">'.format(root)
        xml += dicttoxml.dicttoxml(data, root=False, attr_type=False)
        xml += '<{0}>'.format(root)
        return xml;

    @trace_view
    def post(self, request, format=None):
        resp = {}
        resp['MsgType'] = "SyncAppOrderResp"
        resp['Version'] = "1.0.0"

        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = MobileService(self.request.service_repositories, self.request.activity_repository)
            resp['hRet'] = service.process_charge_order(**serializer.data)
            content = self._xml_encode(resp, "UTF-8", "SyncAppOrderResp")
            return Response(content, content_type="application/xml")
        else:
            resp['hRet'] = 0
            content = self._xml_encode(resp, "UTF-8", "SyncAppOrderResp")
            return Response(content, content_type="application/xml")