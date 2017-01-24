from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='lottery'),
    url(r'item/$', views.LotteryItem.as_view(), name='item'),
    url(r'phone/$', views.LotteryPhone.as_view(), name='phone'),
    url(r'qq/$', views.LotteryQQ.as_view(), name='qq'),
    url(r'latest/$', views.LotteryLatest.as_view(), name='latest'), 
)
