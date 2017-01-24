from django.conf.urls import patterns, url
from card.lobby.apps.iapppay.forms import IapppayForm
import views
from card.lobby.apps.holytree.views import login

iapppay_template_name = {
    'template_name': 'iapppay_login.html',
    'authentication_form': IapppayForm,
}

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='iapppay'),
    url(r'^order/create/$', views.CreateOrder.as_view(), name='iapppay-order-create'),
    url(r'^order/notify/$', views.ChargeNotify.as_view(), name='iapppay-order-notify'),
    url(r'^order/create_holytree/$', views.CreateOrderHolytree.as_view(), name='iapppay-order-create-holytree'),
    url(r'^order/notify_holytree/$', views.ChargeNotifyHolytree.as_view(), name='iapppay-order-notify-holytree'),
    url(r'^order/create_zx/$', views.CreateOrderZX.as_view(), name='iapppay-order-create-zx'),
    url(r'^order/notify_zx/$', views.ChargeNotifyZX.as_view(), name='iapppay-order-notify-zx'),
    url(r'^order/create_zx003/$', views.CreateOrderZX003.as_view(), name='iapppay-order-create-zx003'),
    url(r'^order/notify_zx003/$', views.ChargeNotifyZX003.as_view(), name='iapppay-order-notify-zx003'),
    url(r'^order/create_zx010/$', views.CreateOrderZX010.as_view(), name='iapppay-order-create-zx010'),
    url(r'^order/notify_zx010/$', views.ChargeNotifyZX010.as_view(), name='iapppay-order-notify-zx010'),
    url(r'^order/create_order/$', views.CreateNormalOrder.as_view(), name='iapppay-order-create-order'), #uniform create order url
    url(r'^order/notify_sj04/$', views.ChargeNotifySJ04.as_view(), name='iapppay-order-notify-sj04'),
    url(r'^order/notify_lenovo_duowan/$', views.ChargeNotifyLenovo.as_view(), name='iapppay-order-notify-lenovo-duowan'),
    #url(r'^login/$', login, iapppay_template_name, name='iapppay-login'),
    url(r'^order/notify_fg/$', views.ChargeNotifyFG.as_view(), name='iapppay-order-notify-fg'),
    url(r'^order/notify_sj/$', views.ChargeNotifySJ.as_view(), name='iapppay-order-notify-sj'),
    url(r'^order/notify_hy/$', views.ChargeNotifyHY.as_view(), name='iapppay-order-notify-hy'),
    url(r'^order/notify_ly_qmzjh/$', views.ChargeNotifyLYQMZJH.as_view(), name='iapppay-order-notify-ly-qmzjh'),

)
