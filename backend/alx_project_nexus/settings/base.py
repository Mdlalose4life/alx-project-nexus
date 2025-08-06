import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# GDAL Configuration - MUST be done before any Django imports
if os.name == 'nt':  
    # Set the paths
    gdal_dll_path = config('GDAL_LIBRARY_PATH', default=r'C:\OSGeo4W\bin\gdal311.dll')
    geos_dll_path = config('GEOS_LIBRARY_PATH', default=r'C:\OSGeo4W\bin\geos_c.dll')
    
    # Add OSGeo4W to PATH first
    osgeo_bin = r'C:\OSGeo4W\bin'
    if osgeo_bin not in os.environ.get('PATH', ''):
        os.environ['PATH'] = osgeo_bin + ';' + os.environ.get('PATH', '')
    
    # Set GDAL environment variables
    os.environ['GDAL_DATA'] = r'C:\OSGeo4W\share\gdal'
    os.environ['PROJ_LIB'] = r'C:\OSGeo4W\share\proj'
    
    # Import ctypes to verify DLL can be loaded
    import ctypes
    try:
        # Try to load the GDAL DLL directly
        gdal_lib = ctypes.CDLL(gdal_dll_path)
        print(f"✓ GDAL library loaded successfully: {gdal_dll_path}")
        
        # Set the library path for Django
        os.environ['GDAL_LIBRARY_PATH'] = gdal_dll_path
        os.environ['GEOS_LIBRARY_PATH'] = geos_dll_path
        
    except OSError as e:
        print(f"✗ Failed to load GDAL library: {e}")
        print("Please check your GDAL installation path")
        # Try alternative paths
        alternative_paths = [
            r'C:\OSGeo4W64\bin\gdal311.dll',
            r'C:\Program Files\GDAL\gdal311.dll',
        ]
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                print(f"Found alternative GDAL at: {alt_path}")
                os.environ['GDAL_LIBRARY_PATH'] = alt_path
                break

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

if os.name == 'nt':
    GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
    GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
    
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-change-this')    

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'corsheaders',
    'django_filters',
    'django_extensions',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.businesses',
    'apps.products',
    'apps.orders',
    'apps.locations',
    'apps.reviews',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'alx_project_nexus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

# Spectacular (Swagger/OpenAPI) Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Local Business Directory API',
    'DESCRIPTION': 'A comprehensive API for managing local businesses, products, and user interactions in South African townships and communities.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    
    # # Authentication
    # 'SECURITY_DEFINITIONS': {
    #     'Bearer': {
    #         'type': 'http',
    #         'scheme': 'bearer',
    #         'bearerFormat': 'JWT',
    #     }
    # },
    
    # UI Configuration
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
        'displayRequestDuration': True,
        'docExpansion': 'list',
        'filter': True,
    },
    
    # # Schema generation
    # 'PREPROCESSING_HOOKS': [],
    # 'POSTPROCESSING_HOOKS': [],
    # 'ENUM_NAME_OVERRIDES': {
    #     'ValidationErrorEnum': 'drf_spectacular.utils.ValidationErrorEnum.values',
    # },
    # 'ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE': False,
    
    # # Tags
    # 'TAGS': [
    #     {'name': 'Authentication', 'description': 'User authentication and account management'},
    #     {'name': 'Users', 'description': 'User profile management'},
    #     {'name': 'Businesses', 'description': 'Business listings and management'},
    #     {'name': 'Business Categories', 'description': 'Business category management'},
    #     {'name': 'Products', 'description': 'Product listings and management'},
    #     {'name': 'Product Categories', 'description': 'Product category management'},
    # ],
}


# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    
    "http://localhost:3000",  # React default
    "http://127.0.0.1:3000",
    "http://localhost:8080",  # Vue default
    "http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True