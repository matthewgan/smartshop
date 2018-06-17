# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import GetAddressListView, SetDefaultAddressView, DeleteAddressView, AddAddressView

urlpatterns = [
    url(r'^list/$', GetAddressListView.as_view()),
    url(r'^default/$', SetDefaultAddressView.as_view()),
    url(r'^del/$', DeleteAddressView.as_view()),
    url(r'^add/$', AddAddressView.as_view()),
]