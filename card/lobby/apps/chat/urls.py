from django.conf.urls import patterns, url
from card.lobby.apps.chat import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='chat'),
    url(r'login-chat/$', views.LoginChat.as_view(), name='login-chat'),
)
