# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from faces.views import SearchUserFaceView
from .views import EntranceGetUserInfoView

urlpatterns = [
    url(r'^entry_by_code/$', EntranceGetUserInfoView.as_view()),
    url(r'^entry_by_face/$', SearchUserFaceView.as_view()),

]
