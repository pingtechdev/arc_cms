import logging.handlers
import os
import sys
from pathlib import Path

from corsheaders.defaults import default_headers
from django.http import UnreadablePostError

try:
    from cms_core.local_settings import lsettings
except ImportError:
    lsettings = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-wagtail-cms-secret-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = lsettings.get('DEBUG', os.environ.get('DEBUG', False))
PROD = lsettings.get('PROD', os.environ.get('PROD', True))
DEPLOY_LOCATION = lsettings.get("DEPLOY_LOCATION", "")

ALLOWED_HOSTS = lsettings.get('ALLOWED_HOSTS', os.environ.get('ALLOWED_HOSTS', ['localhost', '127.0.0.1','148.230.122.219','api.arc.pingtech.dev','arc.pingtech.dev']))

# Application definition
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    "corsheaders",
    'compressor',
    
    # Wagtail apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'modelcluster',
    'taggit',
    'rest_framework',
    
    # CMS apps
    'cms_app',  # Our Wagtail content app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    
    # Wagtail middleware
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'cms_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cms_core.wsgi.application'

# Database - FIXED FOR PRODUCTION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'arc_cms',
        'USER': 'arc_user',
        'PASSWORD': 'ARC_cms_deploy_2025',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4', 'use_unicode': True},
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
TEMPLATE_CONTEXT_PROCESSOR = ('django.core.context_processors.i18n',)
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

TIME_ZONE = 'UTC'

# Compress settings
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True

STATIC_URL = lsettings.get("STATIC_URL", "/static/")
STATIC_ROOT = lsettings.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

MEDIA_URL = lsettings.get("MEDIA_URL", "/media/")
MEDIA_ROOT = lsettings.get("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))


# ===================================================
# Logging Settings
# ===================================================
def skip_unreadable_post(record):
    """
    Used in the logging filters callback, to skip UnreadablePostError for the cancelled requests
    """
    if record.exc_info:
        _, exc_value = record.exc_info[:2]
        if isinstance(exc_value, UnreadablePostError):
            return False
    return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "skip_unreadable_posts": {
            "()": "django.utils.log.CallbackFilter",
            "callback": skip_unreadable_post,
        },
    },
    "formatters": {
        "simple": {"format": "%(module)s line: %(lineno)s: %(message)s"},
        "level_module": {
            "format": "%(asctime)s %(levelname)s %(name)s.%(module)s  %(message)s"
        },
        "level_app": {"format": "%(asctime)s | %(levelname)s | %(message)s"},
        "time_message": {"format": "%(asctime)s - %(message)s"},
    },
    "handlers": {
        "email_handler": {"class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "level_app",
        },
        "main_log_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "backupCount": 5,
            "when": "midnight",
            "filename": "%s/cms.log" % lsettings.get("MAIN_LOG_FILE", BASE_DIR),
            "formatter": "level_app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "main_log_file"],
            "level": "ERROR",
            "propagate": True,
        },
        "requests": {
            "handlers": ["console", "main_log_file"],
            "level": "ERROR",
            "propagate": True,
        },
        "wagtail": {
            "handlers": ["console", "main_log_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "": {
            "handlers": ["console", "main_log_file", "email_handler"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
if len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'test', 'shell']:
    print("Resetting loggers to just log on console")
    del LOGGING['handlers']['main_log_file']

    for loggerKey, lgr in LOGGING['loggers'].items():
        if sys.argv[1] in ['runserver', 'test', 'shell']:
            lgr['handlers'] = ['console']
        else:
            lgr['handlers'].remove('main_log_file')

USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en-US', 'English'),
    ('ar-SA', 'Arabic'),
)

LOCALE_PATHS = [os.path.join(PROJECT_PATH, '../locale')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===================================================
# Wagtail CMS Settings
# ===================================================
WAGTAIL_SITE_NAME = 'ARC CMS'
WAGTAILADMIN_BASE_URL = 'http://localhost:8000'

# Allow CORS for API
CORS_ALLOW_ALL_ORIGINS = lsettings.get('CORS_ALLOW_ALL_ORIGINS', DEBUG)
CORS_ALLOWED_ORIGINS = lsettings.get('CORS_ALLOWED_ORIGINS', [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:8080',
    'http://localhost:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'https://arc.pingtech.dev',
    'https://api.arc.pingtech.dev',
])

# Allow custom headers for cache-busting
CORS_ALLOW_HEADERS = list(default_headers) + [
    'cache-control',
    'pragma',
    'expires',
]

# Allow credentials if needed
CORS_ALLOW_CREDENTIALS = True

# REST Framework settings for Wagtail API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://api.arc.pingtech.dev',
    'https://arc.pingtech.dev',
    'http://localhost:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8001',
]

# CSRF Cookie Settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Session Settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Cache Control - Disable caching for API responses in development
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    
    # Add cache control headers to API responses
    MIDDLEWARE = MIDDLEWARE + [
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]

# Wagtail search backend
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Rich text features
WAGTAIL_RICH_TEXT_FIELD_FEATURES = [
    'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 
    'document-link', 'image', 'embed', 'code', 'blockquote'
]

# Wagtail admin customization
WAGTAIL_GRAVATAR_PROVIDER_URL = '//www.gravatar.com/avatar'
WAGTAILADMIN_NOTIFICATION_USE_HTML = True
