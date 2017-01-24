from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='player'),
    url(r'^profile/$', views.ProfileDetails.as_view(), name='profile-details'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetails.as_view()),
    url(r'^refresh/$', views.Refresh.as_view(), name='refresh'),
    url(r'^items/$', views.Items.as_view(), name='items'),
    url(r'^deposit/$', views.Deposit.as_view(), name='deposit'),
    url(r'^withdraw/$', views.Withdraw.as_view(), name='withdraw'),
    url(r'^bank_details/$', views.BankDetails.as_view(), name='bank_details'),
    url(r'^bank_password/$', views.BankPassword.as_view(), name='bank_password'),
    url(r'^update_avatar/$', views.UpdatePlayerAvatar.as_view(), name='update-avatar'),
    url(r'^update_album/$', views.UpdatePlayerAlbum.as_view(), name='update-album'),
    url(r'^delete_album/$', views.DeletePlayerAlbum.as_view(), name='delete-album'),
    url(r'^report_player/$', views.Report.as_view(), name='report-player'),
    url(r'^identify_code/$', views.IdentifyCode.as_view(), name='identify-code'),
    url(r'^identify_idiom/$', views.IdentifyIdiom.as_view(), name='identify-idiom'),
    url(r'^bank_password/forget/$', views.ForgetBankPassword.as_view(), name='forget-bank_password'),
    url(r'^bank_password/reset/$', views.ResetBankPassword.as_view(), name='reset-bank_password'),
    url(r'^vip_bag/draw/$', views.DrawVipBag.as_view(), name='draw-vip-bag'),
    url(r'^before_start/$', views.BeforeStart.as_view(), name='before'),
)
