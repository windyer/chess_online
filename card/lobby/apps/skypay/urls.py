from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='skypay'),
    url(r'^order/create/$', views.CreateOrder.as_view(), name='order-create'),
    url(r'^order/notify/$', views.ChargeNotify.as_view(), name='order-notify'),
 )