# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import ShopListView, ShopCreateView

urlpatterns = [
    url(r'^$', ShopListView.as_view()),
    url(r'^add/$', ShopCreateView.as_view()),
]
