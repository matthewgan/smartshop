# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import GetOrderListView, GetOrderNumView, GetOderDetailView, CancelOrderView, CreateOrderView, CheckForNewOrderView, ConfirmOrderView
from .views import OrderListViewSet

urlpatterns = [
    url(r'^count/$', GetOrderNumView.as_view()),
    url(r'^list/$', GetOrderListView.as_view()),
    url(r'^detail/$', GetOderDetailView.as_view()),
    url(r'^create/$', CreateOrderView.as_view()),
    url(r'^cancel/$', CancelOrderView.as_view()),
    url(r'^checkOrder/$', CheckForNewOrderView.as_view()),
    url(r'^confirm/$', ConfirmOrderView.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', OrderListViewSet.as_view()),
]
