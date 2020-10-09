"""
With these settings, tests run faster.
"""

from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
DJANGO_ENV = 'test'
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = 'nothing-secret-about-this-one'
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "config.testrunner.PytestTestRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# STATIC
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_AUTOREFRESH
WHITENOISE_AUTOREFRESH = True
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# TEMPLATES
# ------------------------------------------------------------------------------
# Overrides to be able to run individual tests from PyCharm
TEMPLATES[-1]["DIRS"].append("/usr/src/app/templates")
