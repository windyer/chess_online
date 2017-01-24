from django.conf.urls import patterns, url
from card.lobby.apps.baidu.forms import BaiduForm
import views
from card.lobby.apps.holytree.views import login
urlpatterns = patterns('',
    url(r'^$', views.api_view, name='api'),
    #url(r'^login/$', views.Login.as_view(), name='login'),
    #url(r'^login/$', login, baidu_template_name, name='login'),
    url(r'^landpage/$', views.LandPage.as_view(), name='landpage'),
)
