from django.conf.urls import url
from .views import CountOrderIntoSaleByTradeNoView, RemoveOrderItemsFromStockView
from .views import SaleQueryByShopView, SaleQueryByMerchandiseView


urlpatterns = [
    # url(r'^add/$', CountOrderIntoSaleByTradeNoView.as_view()),
    # url(r'^sub/$', RemoveOrderItemsFromStockView.as_view()),
    url(r'^shop/(?P<pk>[0-9]+)/$', SaleQueryByShopView.as_view()),
    url(r'^merchandise/(?P<pk>[0-9]+)/$', SaleQueryByMerchandiseView.as_view()),
]