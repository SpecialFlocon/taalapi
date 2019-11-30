from taalapi.settings import *

import os


DEBUG = os.environ['TAALAPI_DEBUG'] or False
SECRET_KEY = os.environ['TAALAPI_SECRET_KEY']

if not DEBUG:
    # Specify hostnames or IP addresses of hosts that are allowed to make requests to this application.
    ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
