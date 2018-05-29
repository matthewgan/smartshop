"""
WSGI config for SmartShop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os,sys

#sys.path.append('home/matthew/wuzhangguishop/SmartShop')
#sys.path.append('home/matthew/wuzhangguishop/venv/lib/python3.5/site-packages')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartShop.settings.production")
#print(sys.path)


from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"]='SmartShop.settings.production'

application = get_wsgi_application()
