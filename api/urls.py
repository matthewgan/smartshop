# Stdlib imports
# Core Django imports
from django.conf.urls import url, include
# Third-party app imports
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated
# Imports from your apps


API_TITLE = 'SmartShop API'
API_DESCRIPTION = 'A Web API for creating and viewing cloud database.'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    # url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION,
                                     authentication_classes=[], permission_classes=[ ],
                                     ),
        ),
    url(r'^token/', include('tokens.urls')),
    url(r'^customer/', include('customers.urls')),
    url(r'^category/', include('categories.urls')),
    url(r'^shop/', include('shops.urls')),
    url(r'^order/', include('orders.urls')),
    url(r'^address/', include('addresses.urls')),
    url(r'^face/', include('faces.urls')),
    url(r'^topup/', include('topups.urls')),
    url(r'^gate/', include('gates.urls')),
    url(r'^merchandise/', include('merchandises.urls')),
    url(r'^tag/', include('tags.urls')),
    url(r'^payment/', include('payments.urls')),
    url(r'^partnervoucher/', include('partnervoucher.urls')),
    # url(r'^inventory/', include('inventory.urls')),
    url(r'^stock/', include('stocks.urls')),
    url(r'^supplier/', include('suppliers.urls')),
    #url(r'^sale/', include('sales.urls')),
]
