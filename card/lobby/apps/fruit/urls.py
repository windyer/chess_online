from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='fruit'),
    url(r'select/(?P<fruit_id>[1-4])/$', views.SelectGame.as_view()),
)
