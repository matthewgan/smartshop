# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .models import Stock
from .views import CreateInStockView, CreateOutStockView, QueryStockView, TransferStockView
from .views import QueryStockByShopView, QueryStockByMerchandiseView


urlpatterns = [
    url(r'in/$', CreateInStockView.as_view()),
    url(r'out/$', CreateOutStockView.as_view()),
    url(r'query/$', QueryStockView.as_view()),
    url(r'transfer/$', TransferStockView.as_view()),
    url(r'^shop/(?P<pk>[0-9]+)/$', QueryStockByShopView.as_view()),
    url(r'^merchandise/(?P<pk>[0-9]+)/$', QueryStockByMerchandiseView.as_view()),
]