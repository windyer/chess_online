from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='roulette'),
    url(r'game/$', views.Roulette.as_view(), name='roulette-game'),
    url(r'record/$', views.RouletteRecord.as_view(), name='roulette-record'),
    url(r'next-roulette-type/$', views.NextRouletteType.as_view(), name='next-roulette-type'),
)
