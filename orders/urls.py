# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import GetOrderListView, GetOrderNumView, GetOderDetailView, SubmitOrderView, CancelOrderView, PayOrderView, PaySuccessView


urlpatterns = [
    url(r'^count/$', GetOrderNumView.as_view()),
    url(r'^list/$', GetOrderListView.as_view()),
    url(r'^detail/$', GetOderDetailView.as_view()),
    url(r'^submit/$', SubmitOrderView.as_view()),
    url(r'^cancel/$', CancelOrderView.as_view()),
    url(r'^pay/$', PayOrderView.as_view()),
    url(r'^paySuccess/$', PaySuccessView.as_view()),
]
