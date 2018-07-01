# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import CustomerSignupView, CustomerLoginView, CustomerListView, CustomerDetailView, CustomerInfoView

urlpatterns = [
    url(r'^signup/$', CustomerSignupView.as_view()),
    url(r'^login/$', CustomerLoginView.as_view()),
    url(r'^list/$', CustomerListView.as_view()),
    url(r'^detail/$', CustomerDetailView.as_view()),
    url(r'^info/$', CustomerInfoView.as_view()),
]
