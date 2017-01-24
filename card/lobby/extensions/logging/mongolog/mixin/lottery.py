from card.lobby.extensions.logging.mongolog import aop
from datetime import datetime
from channel_merge import channel_merge

class LotteryStatistics(object):
    
    @aop.ignore_conn_error
    def lottery_issue(self, user_id, delta, channel, reason, timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp / 1000)
        day = _datetime.date()
        collections = self.mongodb['lottery_issue_' + day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)