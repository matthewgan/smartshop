# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import GetAddressListView, SetDefaultAddressView, DeleteAddressView, AddAddressView

urlpatterns = [
    url(r'^getAddressList/$', GetAddressListView.as_view()),
    url(r'^setDefaultAdd/$', SetDefaultAddressView.as_view()),
    url(r'^deleteAddress/$', DeleteAddressView.as_view()),
    url(r'^addAddress/$', AddAddressView.as_view()),
]