from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from customers.models import Customer
from merchandises.models import Merchandise
from shops.models import Shop
from .models import Stuff


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

           'shop_count': Shop.objects.count(),
           'merchandise_count': Merchandise.objects.count(),
           'area_count': 4800,
           'customer_count': (Customer.objects.count() * 2.5),
           'stuffs': Stuff.objects.all(),
       }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
       request,
       'homepage/contact.html',
       {
           'title': '物掌柜',
           'phone_number': 4006633309,
           'address': '北环西路15号, 金坛区 常州市 江苏省 213000',
           'email': 'info@wuzhanggui.shop',
           'domain': 'www.wuzhanggui.shop',
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
           'title': '物掌柜',
           'phone_number': 4006633309,
           'address': '北环西路15号, 金坛区 常州市 江苏省 213000',
           'email': 'info@wuzhanggui.shop',
           'domain': 'www.wuzhanggui.shop',
           'year': datetime.now().year,
       }
    )
