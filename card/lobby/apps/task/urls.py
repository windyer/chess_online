from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='task'),
    url(r'detail-tasks/$', views.Task.as_view(), name='detail-tasks'),
    url(r'task-config/$', views.TaskConfig.as_view(), name='task-config'),
)
