from datetime import datetime
from card.lobby.extensions.logging.mongolog.aop import ignore_conn_error
from channel_merge import channel_merge


class StoreStatistics(object):
    
    @ignore_conn_error
    def consume_item(self, user_id, channel, app_version, item_id, count, reason, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp/1000)
        day = _datetime.date()
        collections = self.mongodb['consume_item_statistics_'+day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @ignore_conn_error
    def increment_item(self, user_id, channel, app_version, item_id, count, reason, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp/1000)
        day = _datetime.date()
        collections = self.mongodb['increment_item_statistics_'+day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)
        
    @ignore_conn_error
    def sell_item(self, user_id, channel, app_version, item_id, count, gain, reason, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp/1000)
        day = _datetime.date()
        collections = self.mongodb['sell_item_statistics_'+day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @ignore_conn_error
    def send_item(self, user_id, channel, app_version, item_id, count, price, reason, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp/1000)
        day = _datetime.date()
        collections = self.mongodb['send_item_statistics_'+day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)
        
