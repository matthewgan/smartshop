# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .models import Stock
from .views import CreateInStockView, CreateOutStockView, QueryStockView


urlpatterns = [
    url(r'in/$', CreateInStockView.as_view()),
    url(r'out/$', CreateOutStockView.as_view()),
    url(r'query/$', QueryStockView.as_view()),
]