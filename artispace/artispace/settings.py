from pathlib import Path
from decouple import config
import os

# Initialize BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-x0296acpa^t=i!kh&5bgce@-qcp^ag)mh$_g+27pbr#5&9^v_9')
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='').split(',')

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'accounts',  # Make sure the 'accounts' app is present
    'app',       # Your custom app
    'gallery',   # Gallery-related app
    'storages',  # For AWS S3 integration
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',   }
}

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # False means session persists until manually logged out
SESSION_COOKIE_AGE = 86400  # 1 day in seconds

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'app/static']

# Media settings
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_URL = f'https://{config("AWS_STORAGE_BUCKET_NAME")}.s3.amazonaws.com/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS S3 settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='NOT_FOUND')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='NOT_FOUND')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='NOT_FOUND')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_LOCATION = 'media'

# Authentication
# Make sure AUTH_USER_MODEL is only set if you're using a custom user model.
# Uncomment and configure if using custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings (optional)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)

ROOT_URLCONF = 'artispace.urls'  # Replace 'artispace' with your project name if it's different

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = 'customer_dashboard'
LOGIN_REDIRECT_URL = '/artist/dashboard/'
LOGIN_URL = '/customer/login/'  # Set to your customer login URL
LOGIN_REDIRECT_URL = '/customer/dashboard/'  # Redirect to customer dashboard after login