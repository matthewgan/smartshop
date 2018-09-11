# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import SubmitView

urlpatterns = [
    url(r'^add/$', SubmitView.as_view()),
]