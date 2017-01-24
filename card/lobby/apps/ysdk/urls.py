#coding=utf-8
from django.conf.urls import patterns, url
from card.lobby.apps.ysdk.forms import YsdkForm
import views
from card.lobby.apps.holytree.views import login

ysdk_template_name = {
    'template_name': 'ysdk_login.html',
    'authentication_form': YsdkForm
}

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='ysdk'),
    url(r'^login/$', login, ysdk_template_name, name='login'),
    #url(r'^create-order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^create-order/$', views.CreateOrderPayM.as_view(), name='create-order'),
    #url(r'^charge-notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
    url(r'^charge-notify/$', views.ChargeNotifyPayM.as_view(), name='charge-notify'),
)
