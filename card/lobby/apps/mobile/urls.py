from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='mobile'),
    url(r'^charge/notify/$', views.ChargeNotify.as_view(), name='mobile-notify'),
 )