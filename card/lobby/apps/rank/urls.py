from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='rank'),
    url(r'currency/$', views.CurrencyRank.as_view(), name='currency-rank'),
    url(r'gift/$', views.GiftRank.as_view(), name='gift-rank'),
    url(r'today-income-most/$', views.TodayIncomeMost.as_view(), name='today-income-most'),
    url(r'week-fruit-income-most/$', views.WeekFruitIncomeMost.as_view(), name='week-fruit-income-most'),
    url(r'monthly-red-envelope-send-most/$', views.MonthlyRedEnvelopeSendMost.as_view(), name='monthly-red-envelope-send-most'),
    url(r'three-championship/$', views.ThreeChampioship.as_view(), name='three-championship'),
    url(r'fruit-championship/$', views.FruitChampioship.as_view(), name='fruit-championship'),
    url(r'jackpot-most/$', views.JackpotCurrency.as_view(), name='jackpot-most'),
    url(r'jackpot-award/$', views.JackpotAward.as_view(), name='jackpot-award'),
    url(r'self/$', views.UserRanks.as_view(), name='user-ranks'),
)
