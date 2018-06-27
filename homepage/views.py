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
           'title': '物掌柜',
           'phone_number': 4006633309,
           'address': '北环西路15号, 金坛区 常州市 江苏省 213000',
           'email': 'info@wuzhanggui.shop',
           'domain': 'www.wuzhanggui.shop',
           'year': datetime.now().year,

           'shop_count': 2,
           'merchandise_count': 200,
           'area_count': 48000,
           'customer_count': 500,
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
