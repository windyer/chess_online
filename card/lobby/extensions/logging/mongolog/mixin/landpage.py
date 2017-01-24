from card.lobby.extensions.logging.mongolog import aop
from channel_merge import channel_merge


class LandPage(object):

    @aop.ignore_conn_error
    def landpage_download(self,channel,timestamp):
        channel = channel_merge(channel)
        kwargs = locals()
        kwargs.pop('self')
        collections = self.mongodb.landpage_download
        collections.insert(kwargs)
