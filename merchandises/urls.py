# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import QueryMerchandiseDetailByBarcodeView, CreateMerchandiseView

urlpatterns = [
    url(r'^detail/$', QueryMerchandiseDetailByBarcodeView.as_view()),
    url(r'^add/$', CreateMerchandiseView.as_view()),
]