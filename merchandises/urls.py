# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import QueryMerchandiseDetailByBarcodeView, CreateMerchandiseView, QueryMerchandiseDetailByBarcodeForCashierView, QueryMerchandiseDetailByEPCView, QueryMerchandiseDetailByBarcodeForInventoryView


urlpatterns = [
    url(r'^detail/$', QueryMerchandiseDetailByBarcodeView.as_view()),
    url(r'^add/$', CreateMerchandiseView.as_view()),
    url(r'^query/$', QueryMerchandiseDetailByBarcodeForCashierView.as_view()),
    url(r'^tag/$', QueryMerchandiseDetailByEPCView.as_view()),
    url(r'^detailInventory/$', QueryMerchandiseDetailByBarcodeForInventoryView.as_view()),
]
