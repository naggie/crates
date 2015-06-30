from base_settings import *
from os.path import expanduser

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zhj_+x#q-&vqh7&)7a3it@tcsf50@fh9$3&&j0*4pmt1x=ye+1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CAS_DIRECTORY = expanduser('~/crates_cas/')

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
