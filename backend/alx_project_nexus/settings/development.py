from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-123')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': config('DB_NAME', default='alx_project_nexus_dev'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default='password'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# SUPABASE
DATABASES = {
    'default': {  
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('SUPABASE_DB_NAME', default='postgres'),
        'USER': config('SUPABASE_USER', default='postgres.jrtgjsequyibngzzvfvy'),
        'PASSWORD': config('SUPABASE_PASSWORD'), 
        'HOST': config('SUPABASE_URL', default='aws-0-eu-west-2.pooler.supabase.com'),
        'PORT': config('SUPABASE_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',  # SSL is mandatory for Supabase
            'options': '-c search_path=public'  
        },
    }
}

# CORS settings for development
CORS_ALLOWED_ORIGINS += [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']

# Logging
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
        'level': 'DEBUG',
    },
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Celery
CELERY_TASK_ALWAYS_EAGER = True  # Run tasks synchronously in development