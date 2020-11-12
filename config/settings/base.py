"""
Base settings to build other settings files upon.
"""
import environ
import logging
import sentry_sdk

from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration

ROOT_DIR = Path(__file__).parents[2]
APPS_DIR = ROOT_DIR / "apps"
env = environ.Env()

# Load PaaS Service env vars
VCAP_SERVICES = env.json('VCAP_SERVICES', default={})

# GENERAL
# ------------------------------------------------------------------------------
SERVICE_NAME = env("SERVICE_NAME", default="Check International Trade Barriers")
SERVICE_SHORTNAME = env("SERVICE_SHORTNAME", default="CITB")
SERVICE_SUBDOMAIN = env("SERVICE_SUBDOMAIN", default="UKTRADE")
# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

# WSGI
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
BASE_APPS = [
    # apps that need to load first
    'whitenoise.runserver_nostatic',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
]

THIRD_PARTY_APPS = [
    "django_extensions",
]

LOCAL_APPS = [
    "apps.barriers",
    "apps.core",
    "apps.feedback",
    "apps.healthcheck",
    "apps.metadata",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = BASE_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.barriers.middleware.FiltersMiddleware",
    "apps.core.middleware.CookiesMiddleware"
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR / "static/dist"),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "apps.barriers.context_processors.query_params",
                "django.contrib.auth.context_processors.auth",
                # "django.template.context_processors.i18n",
                # "django.template.context_processors.media",
                # "django.template.context_processors.static",
                # "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
            ],
            "builtins": []
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-content-type-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-referrer-policy
SECURE_REFERRER_POLICY = "same-origin"  # the default since Django 3.1
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=60)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = True

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
DJANGO_LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="info").upper()
ELASTIC_APM_ENABLED = env("ELASTIC_APM_ENABLED", default=not DEBUG)
if ELASTIC_APM_ENABLED:
    ELASTIC_APM = {
        "SERVICE_NAME": "market-access-public-fe",
        "SECRET_TOKEN": env("ELASTIC_APM_SECRET_TOKEN"),
        "SERVER_URL": env("ELASTIC_APM_URL"),
        "ENVIRONMENT": env("ENVIRONMENT", default="dev"),
    }
    INSTALLED_APPS.append('elasticapm.contrib.django')

# GOOGLE TAG MANAGER
# ------------------------------------------------------------------------------
GTM_ID = env('GTM_ID')
GTM_AUTH = env('GTM_AUTH')
GTM_PREVIEW = env('GTM_PREVIEW')

# COOKIE SETTINGS
# ------------------------------------------------------------------------------
# More on naming convention
# https://readme.trade.gov.uk/docs/howtos/analytics-cookie-policy.html
COOKIE_SETTINGS_COOKIE_NAME = "cookies_policy"
COOKIE_SETTINGS_EXPIRY = 365  # days
COOKIE_SETTINGS_CONFIRMATION_BANNER = 90  # days
GOOGLE_ANALYTICS_COOKIE_NAME = "usage"
GLOBAL_BAR_SEEN_COOKIE_NAME = "global_bar_seen"
COOKIE_PREFERENCES_SET_COOKIE_NAME = "cookies_preferences_set"


# Settings made available in templates
# ------------------------------------------------------------------------------
# https://github.com/jakubroztocil/django-settings-export#usage
SETTINGS_EXPORT = (
    'COOKIE_PREFERENCES_SET_COOKIE_NAME',
    'COOKIE_SETTINGS_COOKIE_NAME',
    'COOKIE_SETTINGS_CONFIRMATION_BANNER',
    'COOKIE_SETTINGS_EXPIRY',
    'DJANGO_ENV',
    'GOOGLE_ANALYTICS_COOKIE_NAME',
    'GLOBAL_BAR_SEEN_COOKIE_NAME',
    'GTM_ID',
    'GTM_AUTH',
    'GTM_PREVIEW',
    'SERVICE_NAME',
)

# SENTRY
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN", default=None)
if SENTRY_DSN:
    SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        environment=env('SENTRY_ENVIRONMENT'),
        integrations=[
            DjangoIntegration(),
        ],
    )


# Public Data
# ------------------------------------------------------------------------------
PUBLIC_API_GATEWAY_BASE_URI = env("PUBLIC_API_GATEWAY_BASE_URI")


# Forms API
# ------------------------------------------------------------------------------
DIRECTORY_FORMS_API_BASE_URL = env("DIRECTORY_FORMS_API_BASE_URL")
DIRECTORY_FORMS_API_API_KEY = env("DIRECTORY_FORMS_API_API_KEY")
DIRECTORY_FORMS_API_SENDER_ID = env("DIRECTORY_FORMS_API_SENDER_ID")
DIRECTORY_FORMS_API_DEFAULT_TIMEOUT = env.int("DIRECTORY_FORMS_API_DEFAULT_TIMEOUT")
DJANGO_ANONYMOUS_USER_FULL_NAME = env(
    "DJANGO_ANONYMOUS_USER_FULL_NAME", default="Anonymous CITB User"
)
DJANGO_ANONYMOUS_USER_EMAIL = env(
    "DJANGO_ANONYMOUS_USER_EMAIL", default="anonymous.citb.user@service.gov.uk"
)
