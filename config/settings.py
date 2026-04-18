import os
from pathlib import Path
from dotenv import load_dotenv

# =========================

# BASE SETUP

# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))


ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL")  # LOCAL / PRODUCTION

# =========================

# SECURITY

# =========================

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-local-dev-key")

DEBUG = ENVIRONMENT != "PRODUCTION"

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ["artgift.in", "www.artgift.in"]

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# =========================

# CSRF

# =========================

if ENVIRONMENT == "PRODUCTION":
    CSRF_TRUSTED_ORIGINS = [
        "https://artgift.in",
        "https://www.artgift.in",
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    ]

# =========================

# APPLICATIONS

# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
    'users',
    'products',
    'orders',
    'checkout',
    'pages',
    'cart',
    'shipping',
    'analytics',
    

]

# =========================

# MIDDLEWARE

# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =========================

# URL / TEMPLATES

# =========================

ROOT_URLCONF = 'config.urls'

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
            # ✅ keep only ONE cart context
            "cart.context_processors.cart_context",
            "pages.context_processors.site_globals",
            "products.context_processors.categories_context",
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =========================

# DATABASE (AUTO SWITCH)

# =========================


DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =========================

# PASSWORD VALIDATION

# =========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================

# INTERNATIONAL

# =========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =========================

# STATIC & MEDIA

# =========================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================

# CASHFREE

# =========================

CASHFREE_MODE = os.getenv("CASHFREE_MODE", "TEST")
CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY")

if CASHFREE_MODE == "LIVE":
    CASHFREE_BASE_URL = "https://api.cashfree.com/pg"
else:
    CASHFREE_BASE_URL = "https://sandbox.cashfree.com/pg"

# =========================

# MSG91

# =========================

MSG91_AUTH_KEY = os.getenv("MSG91_AUTH_KEY")
MSG91_SENDER_ID = "KARBUI"
MSG91_FLOW_ID = "64f1c9d2a3b2c1abc123456"

# =========================

# SECURITY HARDENING

# =========================

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

if ENVIRONMENT == "PRODUCTION":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# test change