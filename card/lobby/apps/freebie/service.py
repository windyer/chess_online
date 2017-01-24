import hashlib
import time
import collections

import go.logging

from django.conf import settings

from card.core.error.lobby.freebie_error import FreebieError
from card.core.statistics.models import StatisticItem
from card.core.charge import ITEMS

from card.lobby.aop.logging import trace_service
from card.lobby.service.view_service import ViewService
from card.lobby.apps.freebie.redis import SalvageStatus, MoneyTreeStatus
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.timeline.service import TimeLineService
import card.lobby.apps.player.models as player_models
import card.lobby.apps.freebie.models as freebie_models
from card.lobby.apps.freebie.freebie_event import FreebieEvent

@go.logging.class_wrapper
class FreebieService(ViewService):

    def get_salvage_fund(self, user_id):
        status = SalvageStatus()
        salvaged_status = status.get_salvage_info(user_id)

        if salvaged_status['salvage_count'] <= 0:
            raise FreebieError.SALVAGED_ALREADY(user_id=user_id)
        if salvaged_status['next_salvage_time'] > 0:
            raise FreebieError.SALVAGE_FREQUENTLY(user_id=user_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        if profile.currency + profile.bank_currency >= settings.FREEBIE.salvage_currency_criteria:
            raise FreebieError.NOT_POOR_PLAYER(user_id=user_id, currency=profile.currency)

        status.get_salvage_fund(user_id)
        player_currency = player_service.increment_currency(user_id, 
                            settings.FREEBIE.salvage_currency, 'Salvage_currency')

        resp = status.get_salvage_info(user_id)
        resp['currency'] = player_currency.currency
        return resp

    def get_salvage_status(self, user_id):
        stat = SalvageStatus()
        return stat.get_salvage_info(user_id)

    def get_money_tree_status(self, user_id):
        stat = MoneyTreeStatus()
        return stat.money_tree_status(user_id)

    def get_money_tree_award(self, user_id):
        stat = MoneyTreeStatus()
        status = stat.money_tree_status(user_id)
        if not status["can_fetch_now"]:
            raise FreebieError.MONEY_TREE_FETCH_TIME_LIMIT(user_id=user_id)

        stat.get_money_tree_award(user_id)
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        player_currency = player_service.increment_currency(user_id, 
                            settings.FREEBIE.money_tree.award_currency, 'money_tree_currency')

        resp = stat.money_tree_status(user_id)
        resp['currency'] = player_currency.currency
        resp['award_currency'] = settings.FREEBIE.money_tree.award_currency
        return resp

    def _process_youmi_wall_order(self, platform, order, app, ad, adid, user, device, chn, 
                            price, points, time, sig, sign):
        wall_log = freebie_models.YoumiWallLog.get_score_wall_log(order)
        if wall_log is not None:
            raise FreebieError.WALL_ORDER_PROCESSED(order=order)

        if points > 0:
            player_service = PlayerService(self.service_repositories, self.activity_repository)
            player_service.increment_currency(user, points, 'youmi_score_wall')

        wall_log = freebie_models.YoumiWallLog()
        wall_log.platform = platform
        wall_log.order = order
        wall_log.app = app
        wall_log.ad = ad
        wall_log.adid = adid
        wall_log.user = user
        wall_log.device = device
        wall_log.chn = chn
        wall_log.price = price
        wall_log.points = points
        wall_log.time = time
        wall_log.sig = sig
        wall_log.sign = sign
        wall_log.save()

        freebie_event = FreebieEvent(self.service_repositories, self.activity_repository)
        freebie_event.send_score_wall_event(user, points)

    def _process_wall_order(self, user_id, order_id, vender, score, sign):
        wall_log = freebie_models.ScoreWallLog.get_score_wall_log(order_id)
        if wall_log is not None:
            raise FreebieError.WALL_ORDER_PROCESSED(order=order_id)

        player_currency = None
        if score > 0:
            player_service = PlayerService(self.service_repositories, self.activity_repository)
            player_currency = player_service.increment_currency(user_id, score, vender + '_score_wall')

        wall_log = freebie_models.ScoreWallLog()
        wall_log.user_id = user_id
        wall_log.order_id = order_id
        wall_log.vender = vender
        wall_log.score = score
        wall_log.sign = sign
        wall_log.save()

        freebie_event = FreebieEvent(self.service_repositories, self.activity_repository)
        freebie_event.send_score_wall_event(user_id, score)

        return {'award_currency':score, 'currency':player_currency.currency}

    @trace_service
    def process_android_youmi_wall_order(self, order, app, ad, user, device, chn, points, time, sig):
        data = u'{0}||{1}||{2}||{3}||{4}||{5}||{6}'.format(settings.FREEBIE.score_wall.youmi.dev_server_secret, 
                                                    order, app, user, chn, ad, points)[12:20]
        digest = hashlib.md5(data.encode("utf8"))
        if digest.hexdigest() != sig:
            raise FreebieError.WALL_ORDER_AUTH_FAIL(order=order)
        self._process_youmi_wall_order('android', order, app, ad, '', user, device, chn, 
                                0, points, time, '', sig)

    @trace_service
    def process_ios_youmi_wall_order(self, order, app, ad, adid, user, device, 
                                chn, price, points, time, sig, sign):
        data = u"ad={0}adid={1}app={2}chn={3}device={4}order={5}points={6}price={7}sig={8}time={9}user={10}{11}".format(
                ad, adid, app, chn, device, order, points, price, sig, time, user, settings.FREEBIE.score_wall.youmi.dev_server_secret)
        digest = hashlib.md5(data.encode("utf8"))
        if digest.hexdigest() != sign:
            raise FreebieError.WALL_ORDER_AUTH_FAIL(order=order) 
        self._process_youmi_wall_order('ios', order, app, ad, adid, user, device, 
                                    chn, price, points, time, sig, sign)

    @trace_service
    def process_ios_limei_wall_order(self, user_id, order_id, score, sign):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        token = player_extra.token
        adid = settings.FREEBIE.score_wall.limei.adid

        data = "adid={0}score={1}order_id={2}token={3}".format(
                adid, score, order_id, token)

        digest = hashlib.md5(data)
        if unicode(digest.hexdigest()) != sign:
            raise FreebieError.WALL_ORDER_AUTH_FAIL(order=order_id) 
        return self._process_wall_order(user_id, order_id, 'limei', score, sign)

    @trace_service
    def process_ios_domob_wall_order(self, user_id, order_id, score, sign):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        token = player_extra.token
        publisher_id = settings.FREEBIE.score_wall.domob.publisher_id

        data = "publisher_id={0}score={1}order_id={2}token={3}".format(
                publisher_id, score, order_id, token)

        digest = hashlib.md5(data)
        if unicode(digest.hexdigest()) != sign:
            raise FreebieError.WALL_ORDER_AUTH_FAIL(order=order_id) 
        return self._process_wall_order(user_id, order_id, 'domob', score, sign)