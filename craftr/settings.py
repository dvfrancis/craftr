from pathlib import Path
import os
import cloudinary
import dj_database_url
from dotenv import load_dotenv

if os.path.isfile(".env"):
    load_dotenv()

SITE_ID = 1

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Email goes through Amazon SES, which has dominicfrancis.co.uk verified with
# DKIM, so any address on the domain can send.
#
# DEFAULT_FROM_EMAIL was never set, so Django fell back to webmaster@localhost
# and every message was refused by the mail server. Nothing the app sends -
# the contact form, password resets - has ever been delivered.
#
# No credentials are configured: django-ses uses boto3, which picks up the
# EC2 instance role. The role may only send as the address below.
DEFAULT_FROM_EMAIL = 'craftr@dominicfrancis.co.uk'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if not DEBUG:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_SES_REGION_NAME = 'eu-west-2'
    AWS_SES_REGION_ENDPOINT = 'email.eu-west-2.amazonaws.com'
    # django-ses throttles itself by calling ses:GetSendQuota before every
    # send. That action cannot be scoped to a resource, so allowing it would
    # mean granting it account-wide. SES enforces its own rate limit anyway.
    AWS_SES_AUTO_THROTTLE = None

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

# Both lists come from the environment as comma-separated values, so the same
# code runs on Railway and on the AWS box without an edit. The defaults are the
# values that were previously hardcoded here, so leaving the variables unset
# keeps the existing deployment behaving exactly as before.
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "http://127.0.0.1:8000/,https://*.herokuapp.com,"
        "https://*.railway.app,https://*.vercel.app",
    ).split(",") if o.strip()
]

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,.railway.app,.vercel.app",
    ).split(",") if h.strip()
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'home',
    'diary',
    'details',
    'faq',
    'contact',
    'login',
    'register',
    'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Force HTTPS on every generated image URL (issue #113). Without this, images
# were served over http:// on an https:// page, which browsers treat as mixed
# content.
#
# Setting SECURE in the dict above does nothing, which is the trap here.
# django-cloudinary-storage already defaults it to True, but it applies that
# default from cloudinary_storage.app_settings, and that module is only
# imported when something touches the storage backend. CloudinaryField comes
# from cloudinary.models and talks to Cloudinary directly, so STORAGES never
# gets instantiated, the package never loads, and the global config stays at
# secure=None - which the library reads as false.
#
# Configuring it here does not depend on another package's import order.
cloudinary.config(secure=True)

# Media storage is configured in the STORAGES dict, down with the static
# settings, because Django 5.1 collapsed both into that one dict.

MEDIA_URL = '/assets/'
MEDIA_ROOT = os.path.join(BASE_DIR, "assets")

ROOT_URLCONF = 'craftr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'craftr/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'craftr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# This code commented out but kept for future automated testing

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/account/'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# BASE_DIR/'static' has never existed. The only static sources in the repo
# sit under the project package, which is not in INSTALLED_APPS and so is
# never reached by AppDirectoriesFinder either.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'craftr', 'static')]

# Django 5.1 replaced DEFAULT_FILE_STORAGE and STATICFILES_STORAGE with this
# dict. The old names were ignored in silence, which is why STATIC_ROOT holds
# no compressed assets and no staticfiles.json manifest.
#
# staticfiles deliberately uses the non-manifest backend. Manifest storage
# resolves every {% static %} tag through staticfiles.json and raises
# ValueError when the entry is missing, so a deploy that does not run
# collectstatic takes the whole site down rather than one page. Nothing in
# this repo shows whether the box's deploy script runs it. Confirm that
# before switching to CompressedManifestStaticFilesStorage.
STORAGES = {
    # Uploaded images moved to S3 in issue #112. Every row was rewritten from
    # a Cloudinary public ID to a key like classes/<name>.webp by
    # details/0012 and register/0004, so this backend and those migrations
    # have to move together: point this at S3 with the old IDs still in the
    # column, or roll the data back without reverting this, and every image
    # 404s.
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# S3Storage reads these settings itself, so STORAGES above needs no OPTIONS
# block. No credentials appear here: boto3 picks up the EC2 instance role,
# which infra/media-permissions.yaml grants PutObject and GetObject on the
# three upload prefixes and nothing else.
AWS_STORAGE_BUCKET_NAME = os.environ.get(
    'AWS_STORAGE_BUCKET_NAME', 'craftr-dominicfrancis'
)
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-west-2')

# Serve through CloudFront rather than the bucket's own endpoint. The bucket
# blocks all public access, so this is the only route a browser has to it.
AWS_S3_CUSTOM_DOMAIN = os.environ.get(
    'AWS_S3_CUSTOM_DOMAIN', 'media.craftr.dominicfrancis.co.uk'
)

# Unsigned URLs. The objects are public through CloudFront, and signing would
# add a query string that defeats caching for no benefit.
AWS_QUERYSTRING_AUTH = False

# The bucket has ACLs disabled, which is the modern default. Sending one at
# all would be rejected.
AWS_DEFAULT_ACL = None

# Let django-storages rename on collision instead of silently overwriting an
# existing key. It is also why the IAM policy grants GetObject: the check for
# an existing key is a HEAD request.
AWS_S3_FILE_OVERWRITE = False

# Fallbacks for records with no image. These were Cloudinary public IDs built
# into two views at request time; they are now real files in the repository,
# served by WhiteNoise alongside the backgrounds and logo moved in #115.
DEFAULT_CLASS_IMAGE_URL = STATIC_URL + 'craftr/images/class-placeholder.jpg'
DEFAULT_INSTRUCTOR_IMAGE_URL = (
    STATIC_URL + 'craftr/images/instructor-placeholder.jpg'
)
DEFAULT_PROFILE_IMAGE_URL = (
    STATIC_URL + 'craftr/images/profile-placeholder.jpg'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django sends 500 tracebacks to ADMINS by email and prints nothing when
# DEBUG is False. With no ADMINS set, unhandled exceptions vanish entirely.
# Writing to stderr puts them wherever the process log goes - the console in
# development, the systemd journal in production. The app's own loggers are
# covered by root, since its apps are top-level modules rather than sharing a
# package namespace.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
