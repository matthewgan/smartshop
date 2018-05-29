# settings/production.py
from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'masterwudb',
        'USER': 'masterwu',
        'PASSWORD': '@GGx9&JY6Qj$',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

ALLOWED_HOSTS += ('127.0.0.1', 'localhost', '101.132.174.202', 'www.wuzhanggui.shop', 'wuzhanggui.shop', )

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
