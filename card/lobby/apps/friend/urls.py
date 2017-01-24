from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='friend'),
    url(r'friends/$', views.FriendList.as_view(), name='friends'),
    url(r'request/$', views.MakeFriendRequest.as_view(), name='request'),
    url(r'reply/$', views.ReplyFriendRequest.as_view(), name='reply'),
    url(r'break/$', views.BreakFriendship.as_view(), name='break'),
    url(r'send-currency/$', views.FriendSendCurrency.as_view(), name='send-currency'),
    url(r'send-gift/$', views.FriendSendGift.as_view(), name='send-gift'),
    url(r'recommand/$', views.RecommandFriends.as_view(), name='recommand'),
    url(r'send-message/$', views.FriendSendMessage.as_view(), name='send-message'),
)
