from datetime import datetime
from card.lobby.extensions.logging.mongolog import aop
from channel_merge import channel_merge

class ChargeStatistics(object):

    @aop.ignore_conn_error
    @aop.realtime_charge_statistics
    def charge_statistics(self, user_id, item_id, count, price, channel, app_version,
                          reason, item_info, timestamp, is_valid=True):
        channel=channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp/1000)
        day = _datetime.date()
        collections = self.mongodb['charge_statistics_'+day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)
