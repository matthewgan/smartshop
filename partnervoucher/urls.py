# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import CreateVoucherView, ShowVoucherView, VerifyVoucherView


urlpatterns = [
    url(r'^create/$', CreateVoucherView.as_view()),
    url(r'^show/$', ShowVoucherView.as_view()),
    url(r'^verify/$', VerifyVoucherView.as_view()),
]