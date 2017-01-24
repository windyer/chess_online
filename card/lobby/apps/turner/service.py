import time
import uuid
import hashlib

from django.conf import settings

from go.util import DotDict
from go.logging import class_wrapper

from card.core.error.lobby.turner_error import TurnerError
from card.core.property.three import Property

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.extensions.logging import mongo_logger
from card.core.util.timestamp import get_timestamp_for_now

from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.player.models import PlayerExtra
from card.lobby.apps.store.service import StoreService
from card.lobby.apps.turner.turner_session import TurnerSession
from card.lobby.apps.turner.logger import TurnerLogger
from card.lobby.apps.turner.turner_event import TurnerEvent
from card.lobby.apps.activity.base import ActivityHandler
from card.core.util.lottery_key import LotteryFormula
import go.logging
from card.core.error.common import CoreError

@go.logging.class_wrapper
@class_wrapper
class TurnerService(ViewService):

    def __init__(self, service_repositories, activity_repository, counter_repository):
        super(TurnerService, self).__init__(service_repositories, activity_repository)
        self.counter_repository = counter_repository

    def _increment_currency(self,user_id, currency_award):
        if currency_award <= 0:
            return
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        player_currency = player_service.increment_currency(user_id, currency_award, 'turner')

        return player_currency.currency

    def _purchase_turner(self, user_id):
        store_service = StoreService(self.service_repositories, self.activity_repository)
        response = store_service.purchase(user_id, 
                    Property.TURNER_TICKET.item_id, 1, 'turner_tickets')
        cost = response.cost
        if cost != 0:
            extra = PlayerExtra.get_player_extra(user_id)
            mongo_logger.currency_withdrawal(
                user_id=user_id, delta=cost, reason='turner_consume',
                channel=extra.channel,
                timestamp=get_timestamp_for_now(unit='ms'),
                extra_info={'item_id': Property.TURNER_TICKET.item_id,
                            'count': 1}
            )
        return response.currency

    @trace_service
    def turner_begin(self, user_id):
        player_currency = self._purchase_turner(user_id)

        turner_session = TurnerSession.load(user_id)
        if turner_session is not None:
            turner_logger = TurnerLogger()
            turner_logger.record_round_result(user_id, turner_session.award_currency,
                                turner_session.current_round, turner_session.status)
            turner_session.delete()

        good_luck = False
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        if (profile.total_rounds < settings.TURNER.newbie_rounds_criteria or
            int(time.time()) - profile.last_charge_time <= settings.TURNER.charge_interval):
            good_luck = True
        turner_session = TurnerSession.create(user_id, good_luck)
        gaming_status = turner_session.begin()
        gaming_status['currency'] = player_currency

        return gaming_status

    @trace_service
    def turner_gaming(self, user_id, choice, round):
        turner_session = TurnerSession.load(user_id)

        if turner_session is None:
            raise TurnerError.NO_TURNER_SESSION(user_id=user_id)
        if not turner_session.valid_round(round):
            raise TurnerError.INVALID_ROUND(
                user_id=user_id, cur_round=turner_session.current_round, round=round)

        lottery_award = False
        gaming_status = turner_session.gaming(choice)
        if turner_session.status == settings.TURNER.status.win:
            player_currency = self._increment_currency(user_id, turner_session.award_currency)
            turner_event = TurnerEvent(self.service_repositories, self.counter_repository)
            turner_event.send_turner_event(user_id, turner_session.award_currency)
            gaming_status['currency'] = player_currency
            lottery_award = True
            
        if turner_session.game_over:
            turner_logger = TurnerLogger()
            turner_logger.record_round_result(user_id, turner_session.award_currency,
                                turner_session.current_round, turner_session.status)
            turner_session.delete()
        else:
            lottery_award = True

        extra = PlayerExtra.get_player_extra(user_id)
        if settings.LOTTERY.lottery_turner_enable and extra.app_version >= settings.LOTTERY.version and lottery_award:
            lottery_count = LotteryFormula.TurnerFormula(user_id, extra.channel, round + 1)
            if lottery_count != None and lottery_count > 0:
                property_service = self.service_repositories.db.property_service
                transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
                property_service.increment_item(user_id, transaction_id, Property.LOTTERY_TICKET.item_id, lottery_count)
                self.logger.debug("lottery_gain [user_id|%d] [delta|%d] [reason|%s]", user_id, lottery_count, "turner")
                try:
                    player_service = PlayerService(self.service_repositories, self.activity_repository)
                    items = player_service.get_property_items(user_id)
                    total_count = 0
                    for item in items:
                        if item['item_id'] == Property.LOTTERY_TICKET.item_id:                                        
                            total_count = item['count']
                            break

                    bulletin_service = self.service_repositories.chat.bulletin_service
                    bulletin_service.send_lottery_event(user_id=user_id, count=total_count, delta=lottery_count)
                except CoreError.CHAT_CONNECTION_FAILED:
                    pass

        return gaming_status

    @trace_service
    def turner_end(self, user_id):
        turner_session = TurnerSession.load(user_id)
        if turner_session is None:
            raise TurnerError.NO_TURNER_SESSION(user_id=user_id)
        
        turner_session.end()

        award_currency = turner_session.award_currency
        player_currency = self._increment_currency(user_id, award_currency)

        turner_logger = TurnerLogger()
        turner_logger.record_round_result(user_id, award_currency,
                                turner_session.current_round, turner_session.status)

        turner_event = TurnerEvent(self.service_repositories, self.counter_repository)
        turner_event.send_turner_event(user_id, award_currency)

        turner_session.delete()

        resp = {}
        resp['currency'] = player_currency
        resp['status'] = turner_session.status

        ActivityHandler.process_turner(user_id=user_id, 
                                service_repositories=self.service_repositories, 
                                activity_repository=self.activity_repository, 
                                context=DotDict({'award_currency':award_currency}))

        return resp
