from django.conf.urls import patterns, url
from card.lobby.apps.moguwan.forms import MoguwanForm
import views
from card.lobby.apps.holytree.views import login

moguwan_template_name = {
    'template_name': 'moguwan_login.html',
    'authentication_form': MoguwanForm
}


urlpatterns = patterns('',
    url(r'^$', views.api_view, name='moguwan'),
    #url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/$', login, moguwan_template_name, name='login'),
    url(r'^create_order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^charge_notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
)
