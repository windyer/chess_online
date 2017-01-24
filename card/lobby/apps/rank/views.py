from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.conf import settings

import go.logging

from card.core.enum import Rank

from card.lobby import permissions
from card.lobby.aop import api_view_available

import serializers
from service import RankService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'currency': reverse('currency-rank', request=request, format=format),
        'gift': reverse('gift-rank', request=request, format=format),
        'today-income-most': reverse('today-income-most', request=request, format=format),
        'monthly-red-envelope-send-most': reverse('monthly-red-envelope-send-most', request=request, format=format),
        'week-fruit-income-most': reverse('week-fruit-income-most', request=request, format=format),
        'three-championship': reverse('three-championship', request=request, format=format),
        'fruit-championship': reverse('fruit-championship', request=request, format=format),
        'jackpot-most': reverse('jackpot-most', request=request, format=format),
        'jackpot-award': reverse('jackpot-award', request=request, format=format),        
        'self': reverse('user-ranks', request=request, format=format),
        })

@go.logging.class_wrapper
class RankView(generics.ListAPIView):
    permission_classes = (permissions.IsPlayer,)
    paginate_by = 100
    paginate_by_param = 'page_size'
    rank_count = settings.RANK.max_size

    def get_queryset(self):
        service = RankService(self.request.service_repositories, 
                                self.request.activity_repository)
        query_set = service.get_top_rank(self.RANK_NAME, self.rank_count)
        return query_set

    def get(self, request, format=None):
        return super(RankView, self).get(request, format)


@go.logging.class_wrapper
class CurrencyRank(RankView):
    RANK_NAME        = Rank.CURRENCY
    serializer_class = serializers.CurrencyRank

@go.logging.class_wrapper
class GiftRank(RankView):
    RANK_NAME        = Rank.GIFT
    serializer_class = serializers.GiftRank

@go.logging.class_wrapper
class TodayIncomeMost(RankView):
    RANK_NAME        = Rank.TODAY_INCOME_MOST
    serializer_class = serializers.TodayIncomeMost

@go.logging.class_wrapper
class WeekFruitIncomeMost(RankView):
    RANK_NAME        = Rank.FRUIT_WEEK_INCOME_MOST
    serializer_class = serializers.WeekFruitIncomeMost
    rank_count       = 19

@go.logging.class_wrapper
class MonthlyRedEnvelopeSendMost(RankView):
    RANK_NAME        = Rank.RED_ENVELOPE_MONTHLY_SEND_MOST
    serializer_class = serializers.MonthlyRedEnvelopeSendMost
    rank_count       = 19

@go.logging.class_wrapper
class ThreeChampioship(RankView):
    RANK_NAME        = Rank.THREE_WIN_CHAMPIONSHIP
    serializer_class = serializers.ThreeChampionship
    rank_count       = 19

@go.logging.class_wrapper
class FruitChampioship(RankView):
    RANK_NAME        = Rank.FRUIT_WIN_CHAMPIONSHIP
    serializer_class = serializers.FruitChampionship
    rank_count       = 19

@go.logging.class_wrapper
class JackpotAward(RankView):
    RANK_NAME        = Rank.JACKPOT_AWARD
    serializer_class = serializers.JackpotAward
    rank_count       = 29

@go.logging.class_wrapper
class JackpotCurrency(RankView):
    RANK_NAME        = Rank.JACKPOT_CURRENCY
    serializer_class = serializers.JackpotCurrency
    rank_count       = 9

@go.logging.class_wrapper
class UserRanks(generics.ListAPIView):
    permission_classes = (permissions.IsPlayer,)

    def get(self, request, format=None):
        service = RankService(self.request.service_repositories, 
                                self.request.activity_repository)
        user_ranks = service.get_user_ranks(self.request.user.id)

        return Response(user_ranks)
