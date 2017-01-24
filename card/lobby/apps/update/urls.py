from django.conf.urls import patterns, url

from card.lobby.apps.update import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='update'),
    url(r'^latest/(?P<platform>\w+)/(?P<channel>\w+)/(?P<version>\d+[\.\d+]*)/$', views.LatestVersion.as_view()),
)