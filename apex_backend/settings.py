from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me'

DEBUG = False

ALLOWED_HOSTS = [
    'RikoNaito.pythonanywhere.com',
    'localhost',
    '127.0.0.1',

]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'core',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_ORIGINS =[
    "https://apexcreatives.netlify.app",
    "https://localhost:5500",
    "https://127.0.0.1:5500",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'apex_backend.urls'

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

WSGI_APPLICATION = 'apex_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER =  'apexcreativesteam@gmail.com' # Your company email
EMAIL_HOST_PASSWORD = 'qqpcncxkbqkwgbys'  # App password (not regular password)
DEFAULT_FROM_EMAIL = 'apexcreativesteam@gmail.com'

# Where to send contact form submissions
CONTACT_RECIPIENT_EMAIL = 'apexcreativesteam@gmail.com'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = 'home/RikoNaito/apexbackend/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/RikoNaito/apexbackend/media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
