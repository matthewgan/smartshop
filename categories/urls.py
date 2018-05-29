# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports

# Imports from your apps
from .views import CategoryListView
from merchandises.views import MerchandisesShowByCategoryView

urlpatterns = [
    url(r'^$', CategoryListView.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', MerchandisesShowByCategoryView.as_view()),
]
