from django.conf.urls import patterns, url
import views
from card.lobby.apps.huawei.forms import HuaweiForm
from card.lobby.apps.holytree.views import login

huawei_template_name = {
    'template_name': 'huawei_login.html',
    'authentication_form': HuaweiForm
}

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='huawei'),
    url(r'^login/$', login, huawei_template_name, name='login'),
    url(r'^create_order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^charge_notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
)
