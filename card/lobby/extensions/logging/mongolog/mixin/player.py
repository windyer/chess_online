from card.lobby.extensions.logging.mongolog import aop
from datetime import datetime
from channel_merge import channel_merge


class PlayerStatistics(object):

    @aop.ignore_conn_error
    @aop.realtime_login_statistics
    def player_login(self, user_id, nick_name, currency, device_id, device_name,
                     device_model, app_version, version_updated, login_ip,
                     os_version, channel, vender, timestamp):
        if channel is None:
            return
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['player_login_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    @aop.realtime_register_statistics
    def player_register(self, user_id, nick_name, player_type, app_version,
                        os_version, os_platform, device_id, channel, vender,
                        login_ip, timestamp, silent_user=True):
        if channel is None:
            return
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['player_register_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    def online_period(self, user_id, channel, start_timestamp, end_timestamp, app_version):
        if channel is None:
            return
        channel = channel_merge(channel)
        assert start_timestamp <= end_timestamp
        kwargs = locals()
        kwargs.pop('self')
        kwargs['online_time'] = end_timestamp - start_timestamp
        _datetime = datetime.fromtimestamp(start_timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['player_online_period_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)
