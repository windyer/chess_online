from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='zhuoyi'),
    url(r'^order/create/$', views.CreateOrder.as_view(), name='zhuoyi-order-create'),
    url(r'^order/notify/$', views.ChargeNotify.as_view(), name='zhuoyi-order-notify'),
    url(r'^order/create_order/$', views.CreateOrderNormal.as_view(), name='zhuoyi-order-create-order'),
    url(r'^order/notify_zx/$', views.ChargeNotifyZX.as_view(), name='zhuoyi-order-notify-zx'),
    url(r'^order/notify_uuu/$', views.ChargeNotifyUUU.as_view(), name='zhuoyi-order-notify-uuu'),

)
