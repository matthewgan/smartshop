# Stdlib imports

# Core Django imports
from django.conf.urls import url

# Third-party app imports
from rest_framework.authtoken import views

# Imports from your apps

urlpatterns = [
    url(r'^get_auth_token/$', views.obtain_auth_token, name="get_auth_token"),
]