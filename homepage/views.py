from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime


# Create your views here.
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
       request,
       'homepage/index.html',
       {
           'title': 'Home Page',
           'year': datetime.now().year,
       }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
       request,
       'homepage/contact.html',
       {
           'title': 'Contact',
           'message': 'Your contact page.',
           'year': datetime.now().year,
       }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
       request,
       'homepage/about.html',
       {
           'title': 'About',
           'message': 'Your application description page.',
           'year': datetime.now().year,
       }
    )
