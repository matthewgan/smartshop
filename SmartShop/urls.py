"""SmartShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Stdlib imports
from datetime import datetime
# Core Django imports
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout
# Third-party app imports
# Imports from your apps
import homepage.views
import homepage.forms

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homepage.views.home, name='home'),
    url(r'^contact$', homepage.views.contact, name='contact'),
    url(r'^about', homepage.views.about, name='about'),
    url(r'^login/$', login,
        {
            'template_name': 'homepage/login.html',
            'authentication_form': homepage.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$', logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
