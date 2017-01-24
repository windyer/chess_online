from card.lobby.extensions.logging.mongolog import aop
from datetime import datetime
from channel_merge import channel_merge

class CurrencyStatistics(object):
    
    @aop.ignore_conn_error
    @aop.realtime_currency_statistics
    def currency_issue(self, user_id, delta, reason, channel, timestamp,
                       extra_info=None):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['currency_issue_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    @aop.realtime_currency_statistics
    def currency_withdrawal(self, user_id, delta, reason, channel, timestamp,
                            extra_info=None):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['currency_withdrawal_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    def currency_liquidity(self, user_id, mode_level, channel,
                           stake=0, raise_challenge=0, gift=0,
                           three_system_dealer_win_expectation=0,
                           three_system_dealer_lose_expectation=0, timestamp=None):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['currency_liquidity_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    def jackpot_withdrawal(self, user_id, delta, channel, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['jackpot_withdrawal_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    @aop.realtime_currency_statistics
    def jackpot_issue(self, user_id, delta, channel, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['jackpot_issue_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)

    @aop.ignore_conn_error
    def cat2currency(self, user_id, delta, channel, weight, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        kwargs.pop('timestamp')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['cat2currency_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)