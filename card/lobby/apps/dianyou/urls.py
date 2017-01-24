from django.conf.urls import patterns, url
from card.lobby.apps.dianyou.forms import DianYouForm
import views
from card.lobby.apps.holytree.views import login

yuyang_template_name = {
    'template_name': 'dianyou_login.html',
    'authentication_form':DianYouForm
}


urlpatterns = patterns('',
    url(r'^$', views.api_view, name='dianyou'),
    #url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/$', login, yuyang_template_name, name='login'),
    url(r'^create-order/$', views.CreateOrder.as_view(), name='create-order'),
    url(r'^charge-notify/$', views.ChargeNotify.as_view(), name='charge-notify'),
)
