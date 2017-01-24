from django.conf import settings
from go.logging import class_wrapper


@class_wrapper
class UpdateService(object):

    def get_latest_version(self, platform, version, channel):
        resp = {}
        if platform not in settings.UPDATE:
            resp["is_active"] = False
            return resp

        if channel not in settings.UPDATE[platform].channels:
            configure = settings.UPDATE[platform].default
        else:
            configure = settings.UPDATE[platform].channels[channel]

        if configure.init_start:
            resp["init_start"] = True
        elif configure.is_active:
            resp["is_active"] = True
            resp["version"] = configure.cur.version
            resp["force_upgrade"] = configure.cur.force_upgrade
            resp["force_degrade"] = configure.cur.force_degrade
            resp["delta_update"] = configure.cur.delta_update
            resp["url_prefix"] = configure.cur.url_prefix
            resp["desc"] = configure.cur.desc
        else:
            resp["is_active"] = False
            resp['version'] = configure.cur.version
            resp['force_upgrade'] = configure.cur.force_upgrade

        return resp
