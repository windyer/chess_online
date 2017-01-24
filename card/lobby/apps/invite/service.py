from card.lobby.service.view_service import ViewService
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.player.models import Player,PlayerExtra
from django.conf import settings
from go.containers import redis
from go.containers.containers import Hash,List,SortedSet
import time
from card.core.error.lobby import InviteError
import go.logging
from card.lobby.aop.logging import trace_service

@go.logging.class_wrapper
class InviteService(ViewService):
    def __init__(self, service_repositories, activity_repository):
        super(InviteService, self).__init__(service_repositories, activity_repository)

    @trace_service
    def invite_info(self,user_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        key = settings.INVITE.redis_list_key.format(user_id)
        _listed = List(key, db=re)
        inviters_list = _listed.members
        try:
            inviter = inviters_list[-1]
        except:
            inviter = 0
        date={'QR_code':settings.INVITE.QR_code,'down_url':settings.INVITE.down_url,'inviter':inviter}
        return date

    @trace_service
    def set_inviter(self, user_id, inviter_id):
        try:
            inviter_extra = PlayerExtra.get_player_extra(inviter_id)
            creat_inviter_time = inviter_extra.created_time
        except:
            raise InviteError.NO_INVITE_ID(inviter_id=inviter_id)
        user_extra = PlayerExtra.get_player_extra(user_id)
        creat_user_time = user_extra.created_time
        if creat_user_time <= creat_inviter_time:
            raise InviteError.INVITER_IS_NEW_PLAYER(inviter_id=inviter_id)
        re = redis.Redis(**settings.PERSIST_REDIS)
        inviter_key = settings.INVITE.redis_list_key.format(inviter_id)
        inviter_listed = List(inviter_key, db=re)
        inviters_list = inviter_listed.members
        if len(inviters_list)>=1:
            second_inviter=inviters_list[-1]
        else:
            second_inviter=''
        inviters_list.append(inviter_id)
        re = redis.Redis(**settings.PERSIST_REDIS)
        user_key = settings.INVITE.redis_list_key.format(user_id)
        user_listed = List(user_key, db=re)
        if user_listed.llen() != 0:
            raise InviteError.HAS_DONE_INVITED(inviter_id=inviter_id, user_id=user_id)
        user_listed.extend(inviters_list)
        inviter_key = settings.INVITE.redis_hash_key.format(inviter_id)
        inviter_hashed = Hash(inviter_key, db=re)
        inviter_hashed.hincrby("invite_count",1)
        if second_inviter != '':
            second_inviter_key = settings.INVITE.redis_hash_key.format(second_inviter)
            second_inviter_hashed = Hash(second_inviter_key, db=re)
            second_inviter_hashed.hincrby("invite_count", 1)
        return {'inviter_id':inviter_id}

    @trace_service
    def award_info(self, user_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        user_key = settings.INVITE.redis_hash_key.format(user_id)
        user_hashed = Hash(user_key, db=re)
        not_receive_award = user_hashed.hget('not_receive_award')
        if not_receive_award is None:
            not_receive_award = 0
        received_award = user_hashed.hget('received_award')
        if received_award is None:
            received_award = 0
        invite_count = user_hashed.hget('invite_count')
        if invite_count is None:
            invite_count = 0
        total_award = int(not_receive_award) + int(received_award)
        user_sorted = SortedSet(settings.INVITE.redis_bull_key)
        bull_list=user_sorted.zrevrange(0,29)
        bulls=[]
        for bull in bull_list:
            one_bull_list = bull.split(":")
            bulls.append({one_bull_list[0]:one_bull_list[1]})
        award_info = {'not_receive_award':not_receive_award,'total_award':total_award,'invite_count':invite_count,'bulls':bulls}
        return award_info

    @trace_service
    def get_award(self, user_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        user_key = settings.INVITE.redis_hash_key.format(user_id)
        user_hashed = Hash(user_key, db=re)
        not_receive_award = user_hashed.hget('not_receive_award')
        if not_receive_award is None:
            raise InviteError.NO_AWARDS(user_id=user_id)
        user_hashed.hincrby('received_award',int(not_receive_award))
        received_award = user_hashed.hget('received_award')
        user_hashed.hset('not_receive_award',0)
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        player_service.increment_currency(user_id,int(not_receive_award),settings.INVITE.reason)
        player = Player.get_player(user_id)
        nick_name = player.nick_name
        user_sorted = SortedSet(settings.INVITE.redis_bull_key)
        user_sorted.zadd(nick_name+':'+str(received_award),str(time.time()))
        return {'currency':not_receive_award}
