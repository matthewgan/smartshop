# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import TagCreateView, TagQueryView, TagDeleteView, TagStatusUpdateView

urlpatterns = [
    url(r'^add/$', TagCreateView.as_view()),
    url(r'^delete/$', TagDeleteView.as_view()),
    url(r'^query/$', TagQueryView.as_view()),
    url(r'^update/$', TagStatusUpdateView.as_view()),
]

