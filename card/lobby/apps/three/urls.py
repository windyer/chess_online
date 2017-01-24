from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='three'),
    url(r'select/(?P<three_id>[1-4])/$', views.SelectGame.as_view()),
)
