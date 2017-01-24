from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.api_view, name='wiipay'),
                       url(r'^order/create/$', views.CreateOrder.as_view(), name='wiipay-order-create'),
                       url(r'^order/notify_zx001/$', views.ChargeNotify.as_view(), name='wiipay-order-notify-zx001'),
                       url(r'^order/notify_zx002/$', views.ChargeNotify_ZX002.as_view(), name='wiipay-order-notify-zx002'),
                       )
