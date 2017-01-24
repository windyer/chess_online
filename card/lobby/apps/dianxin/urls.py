from django.conf.urls import patterns, url
import views
from card.lobby.apps.holytree.views import login


urlpatterns = patterns('',
    url(r'^$', views.api_view, name='dianxin'),
    #url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^create-order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^charge-notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
)
