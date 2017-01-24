from pymongo import MongoClient

import go.logging

from card.core.conf import settings
from mixin import (
    PlayerStatistics, ChargeStatistics, CurrencyStatistics,
    ConversionStatistics, LotteryStatistics, BullDownloadStatistics,LandPage
)


class BaseLogger(object):

    def __init__(self):
        self.client = None

    @property
    def mongodb(self):
        if self.client is None:
            self.client = MongoClient(**settings.MONGO_CONN)
        return self.client[settings.MONGO_DB]


@go.logging.class_wrapper
class MongoLogger(BaseLogger, PlayerStatistics, ChargeStatistics,
                  CurrencyStatistics, ConversionStatistics, LotteryStatistics,
                  BullDownloadStatistics,LandPage):
    pass


mongo_logger = MongoLogger()
