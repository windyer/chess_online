from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='game'),
    url(r'quick/$', views.QuickGame.as_view(), name='quick-game'),
    #url(r'select/$', views.SelectGame.as_view(), name='select-game'),
    url(r'select/(?P<mode>[1-4])/(?P<level>[1-3])/$', views.SelectGame.as_view()),
    url(r'follow/(?P<target_user_id>\d+)/$', views.FollowGame.as_view()),
)
