# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import GetTencentNotifyView


urlpatterns = [
    url(r'^notify/$', GetTencentNotifyView.as_view()),
]