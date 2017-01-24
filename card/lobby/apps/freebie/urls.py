from django.conf.urls import patterns, url
from card.lobby.apps.freebie import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='freebie'),
    url(r'salvage/$', views.Salvage.as_view(), name='salvage'),
    url(r'money_tree/$', views.MoneyTree.as_view(), name='money-tree'),
    url(r'wall/ios/youmi/$', views.YoumiIosWall.as_view(), name='youmi-ios-wall'),
    url(r'wall/android/youmi/$', views.YoumiAndroidWall.as_view(), name='youmi-android-wall'),
    url(r'wall/ios/domob/$', views.DomobIosWall.as_view(), name='domob-ios-wall'),
    url(r'wall/ios/limei/$', views.LimeiIosWall.as_view(), name='limei-ios-wall'),
)