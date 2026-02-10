from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your_default_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Update ALLOWED_HOSTS for development and production
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'yourdomain.com', 'www.yourdomain.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Your main application
    'staff',  # Your staff application
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # This is important
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'djangoan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'djangoan.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'courier',
        'USER': 'root',
        'PASSWORD': 'augustineANNA020628',
        'HOST': 'localhost',
        'PORT': '3306',
    }
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory to collect static files

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Use the appropriate SMTP server
EMAIL_PORT = 587  # Use 587 for TLS or 465 for SSL
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'annaantony0306@gmail.com')  # Replace with your email
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your_app_password')  # Use an app password if 2FA is enabled
EMAIL_USE_TLS = True  # Set to True for TLS, or use EMAIL_USE_SSL = True for SSL

# Redirect URL after successful login
LOGIN_REDIRECT_URL = '/staff/dashboard/'  # Change this to the desired redirect URL after login
LOGIN_URL = '/staff/'  # This should point to your custom login view
LOGIN_URL = '/myapp/signin/'  # Redirect to the sign-in page if not logged in
LOGIN_REDIRECT_URL = '/myapp/dashboard/'  # Redirect to the dashboard after login
LOGIN_REDIRECT_URL = '/myapp/' 
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py
SESSION_COOKIE_AGE = 1209600  # 2 weeks, in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False