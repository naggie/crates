from base_settings import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zhj_+x#q-&vqh7&)7a3it@tcsf50@fh9$3&&j0*4pmt1x=ye+1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.']

# where will nginx look for static files for production?
# collect all static files by running ./manage.py collectstatic
STATIC_URL = '/static/'
STATIC_ROOT = '{{crates_dir}}'


CAS_DIRECTORY = abspath('{{cas_dir}}')

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# http://wiki.nginx.org/XSendfile
# Faster serving of CAS files. Backed by nginx using Django to authenticate the
# request.
X_SENDFILE = True
