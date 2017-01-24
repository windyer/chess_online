from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='invite'),
    url(r'^invite_info/$', views.InviteInfo.as_view(), name='invite-info'),
    url(r'^award_info/$', views.AwardInfo.as_view(), name='award-info'),
    url(r'^set_inviter/$', views.SetInviter.as_view(), name='set-inviter'),
    url(r'^get_award/$', views.GetAward.as_view(), name='get-award'),
)

