from datetime import datetime
from card.lobby.extensions.logging.mongolog import aop
from channel_merge import channel_merge


class BullDownloadStatistics(object):

    @aop.ignore_conn_error
    def bull_download(self, user_id, channel, download, timestamp):
        channel=channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        _datetime = datetime.fromtimestamp(timestamp/1000)
        day = _datetime.date()
        collections = self.mongodb['bull_download_'+day.strftime('%Y_%m_%d')]
        collections.insert(kwargs)
