# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import SubmitView, PriceEditView

urlpatterns = [
    url(r'^add/$', SubmitView.as_view()),
    url(r'^edit/$', PriceEditView.as_view()),
]