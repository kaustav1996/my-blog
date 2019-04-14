# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '_nc9_+ntllx!ptq5tzh96nn^$a#81#auhrdw#8t#+n0#4ig(lz'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_blog_it.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'simple_pagination',
    'django_blog_it.django_blog_it',
    'django_blog_it.posts',
    # 'django_blog_it.payments.apps.PaymentsConfig',
    'django_blog_it.payments',
)



if 'ON_HEROKU' in os.environ:
    import dj_database_url

    DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
    }
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mydb',
            'USER': 'postgres',
            'PASSWORD': 'kaustav@123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }




ALLOWED_HOSTS = ["127.0.0", "localhost","*"]
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
DEBUG = True
EMAIL_PORT    = 465
EMAIL_HOST    = 'smtp.gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'kaustavsmailbox21@gmail.com'
EMAIL_HOST_PASSWORD = 'kaustav@432123'
STRIPE_SECRET_KEY = 'sk_test_j8ULflzHxbsXvSMaEHAGXFVl003H8o86RT'
STRIPE_PUBLISHABLE_KEY = 'pk_test_ivFuxlMPRIwblreWKSoYKT8f00TsVpGygT'
