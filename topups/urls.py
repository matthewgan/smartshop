# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import TopupCreateView, ShowGiftView
from .views import TopUpSuccessView, PointToBalanceView, checkTopUpView

urlpatterns = [
    url(r'^$', TopupCreateView.as_view()),
    url(r'^gift/$', ShowGiftView.as_view()),
    url(r'^success/$', TopUpSuccessView.as_view()),
    url(r'^point/$', PointToBalanceView.as_view()),
    url(r'^check/$', checkTopUpView.as_view()),
]
