from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mahila_pratinidhi',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
#
# INSTALLED_APPS += [
#
#     'debug_toolbar',
#
# ]
#
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
#
# ]
# INTERNAL_IPS = '127.0.0.1'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]

STATIC_ROOT = os.path.join(BASE_DIR, 'a-static')