# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import RegisterFaceView, SearchUserFaceView, FaceRegisterView

urlpatterns = [
    url(r'^register/$', FaceRegisterView.as_view()),
    url(r'^search/$', SearchUserFaceView.as_view()),
]
