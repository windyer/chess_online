from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='turner'),
    url(r'^begin/$', views.TurnerBegin.as_view(), name='begin'),
    url(r'^gaming/$', views.TurnerGaming.as_view(), name='gaming'),
    url(r'^end/$', views.TurnerEnd.as_view(), name='end'),
)
