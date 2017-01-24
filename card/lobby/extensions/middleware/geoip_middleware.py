__all__ = ['GeoIpMiddleware']

import geoip2.database
from django.conf import settings

class GeoIpMiddleware(object):

    geoip_reader = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path.startswith(settings.STATIC_URL):
            if GeoIpMiddleware.geoip_reader is None:
                GeoIpMiddleware.geoip_reader = geoip2.database.Reader(settings.GEOIP_FILE)
            request.geoip_reader = GeoIpMiddleware.geoip_reader