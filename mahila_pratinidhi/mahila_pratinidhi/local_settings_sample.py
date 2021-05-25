from .settings import *

ALLOWED_HOSTS = ['mahilapratinidhi.naxa.com.np', 'mahilapratinidhi.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
SECRET_KEY = 'm#6kgs*ve1@-xu$zf0y+^3mo_8af*bveqjus32x)m#6kgs*ve1@-xu$24gmy2emnx'
DEBUG = True

STATICFILES_DIRS = [
#        os.path.join(BASE_DIR, "static")
    ]
#
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
