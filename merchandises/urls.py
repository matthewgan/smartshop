# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import QueryMerchandiseDetailByBarcodeView, CreateMerchandiseView
from .views import QueryMerchandiseDetailByBarcodeForCashierView, QueryMerchandiseDetailByEPCView
from .views import QueryMerchandiseDetailByBarcodeForInventoryView
from .views import MerchandiseDetailView


urlpatterns = [
    url(r'^detail/$', QueryMerchandiseDetailByBarcodeView.as_view()),
    url(r'^add/$', CreateMerchandiseView.as_view()),
    url(r'^query/$', QueryMerchandiseDetailByBarcodeForCashierView.as_view()),
    url(r'^tag/$', QueryMerchandiseDetailByEPCView.as_view()),
    # url(r'^detailInventory/$', QueryMerchandiseDetailByBarcodeForInventoryView.as_view()),
    url(r'^fast_query/$', QueryMerchandiseDetailByBarcodeForInventoryView.as_view()),
    url(r'(?P<pk>[0-9]+)/$', MerchandiseDetailView.as_view()),
]
