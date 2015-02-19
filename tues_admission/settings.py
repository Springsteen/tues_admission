import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'o)z_$9&mbvt4zs&l0xo7=xj_5j^zhud9br)ddq3l12fb20nzw_'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'south',
    'social.apps.django_app.default',

    'campaigns',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tues_admission.urls'

WSGI_APPLICATION = 'tues_admission.wsgi.application'


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/tues-admission-752:admission-sql-db',
            'NAME': 'admission_sql_db',
            'USER': 'root',
        }
    }
elif os.getenv('SETTINGS_MODE') == 'prod':
    SOUTH_DATABASE_ADAPTERS = {
        'default': 'south.db.postgresql_psycopg2'
    }
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': 'tues-admission-752:admission-sql-db',
            'NAME': 'admission_sql_db',
            'USER': 'root',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '890110708365-boaltcp16pb7b2ungo38jaoqmk4ilrrq.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'VJFNRyKyqLlmNQq64TYEK_xa'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://tues-admission-752.appspot.com/campaigns'

#get all user mails and put them into google oauth2 whitelist so they can log with google acc
from django.contrib.auth.models import User
whitelist = [x for x in User.objects.filter(is_staff=True).values_list('email', flat=True) if x]

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = whitelist

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
