from django.conf.urls import patterns, url
from card.lobby.apps.chubao.forms import ChubaoForm
import views
from card.lobby.apps.holytree.views import login

chubao_template_name = {
    'template_name': 'chubao_login.html',
    'authentication_form': ChubaoForm
}


urlpatterns = patterns('',
    url(r'^$', views.api_view, name='chubao'),
    #url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/$', login, chubao_template_name, name='login'),
    url(r'^create-order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^charge-notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
)
