from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.api_view, name='store'),
    url(r'purchase/$', views.PurchaseItem.as_view(), name='purchase-item'),
    url(r'sell/$', views.SellItem.as_view(), name='sell-item'),
    url(r'bull-url/$', views.BullUrl.as_view(), name='bull-url'),
    url(r'bull-complete/$', views.BullComplete.as_view(), name='bull-complete'),
    url(r'store-item/$', views.StoreItem.as_view(), name='store-item'),
)
