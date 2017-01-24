from django.conf.urls import patterns, url
from card.lobby.apps.daily import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='daily'),
    url(r'award/$', views.Daily.as_view(), name='award'),
    url(r'award-online/$', views.OnlineAward.as_view(), name='online-award'),
    )
