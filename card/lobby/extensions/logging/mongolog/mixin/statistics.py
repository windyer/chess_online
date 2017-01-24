from card.lobby.extensions.logging.mongolog.aop import ignore_conn_error
from datetime import datetime
from channel_merge import channel_merge


class ConversionStatistics(object):

    @ignore_conn_error
    def daily_award_conversion(self, user_id, channel, first_day_login, quit_type,
                    can_draw_award, timestamp, scene='daily_award'):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['daily_award_conversion_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @ignore_conn_error
    def charge_recommend_conversion(self, user_id, channel, first_day_login, quit_type,
                         item_id, timestamp, scene='charge_recommend'):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['charge_recommend_conversion_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @ignore_conn_error
    def newbie_guide_conversion(self, user_id, channel, first_day_login, quit_type,
                     timestamp, scene='newbie_guide'):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['newbie_guide_conversion_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @ignore_conn_error
    def monthly_payment_subscribe(self, user_id, channel, item_id, timestamp,
                                  reason='subscribe'):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['monthly_payment_subscribe_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @ignore_conn_error
    def monthly_payment_unsubscribe(self, user_id, channel, timestamp,
                                    reason='unsubscribe'):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['monthly_payment_unsubscribe_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)
