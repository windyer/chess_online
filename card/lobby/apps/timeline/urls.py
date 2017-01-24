from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.api_view, name='timeline'),
                       url(r'friend-trends/(?P<page>\d+)/$', views.FriendTrend.as_view(), name='friend-trends'),
                       url(r'personal-message/(?P<page>\d+)/$', views.PersonalMessage.as_view(), name='personal-message'),
                       url(r'friend-message/(?P<peer_user_id>\d+)/(?P<page>\d+)/$', views.FriendMessage.as_view(), name='friend-message'),
                       url(r'system-message/$', views.SystemMessage.as_view(), name='system-message'),
                       url(r'del-friend-message/$', views.DelFriendMessage.as_view(), name='del-friend-message'),
                       url(r'system-push/(?P<device_id>\w+)/$', views.SystemPush.as_view(), name='system-push'),
                       url(r'unread-system-message/$', views.UnreadSystemMessage.as_view(), name='unread-system-message'),
                       )
