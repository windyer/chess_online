from django.conf.urls import patterns, url
from card.lobby.apps.coolpad.forms import CoolpadForm
import views
from card.lobby.apps.holytree.views import login

coolpad_template_name = {
    'template_name': 'coolpad_login.html',
    'authentication_form': CoolpadForm
}


urlpatterns = patterns('',
    url(r'^$', views.api_view, name='coolpad'),
    #url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/$', login, coolpad_template_name, name='login'),
    url(r'^create-order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^charge-notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
)
