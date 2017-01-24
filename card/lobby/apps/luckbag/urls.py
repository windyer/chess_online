from django.conf.urls import patterns, url
from card.lobby.apps.luckbag import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='luckbag'),
    url(r'open_bag/$', views.LuckBag.as_view(), name='open_bag'),
    )