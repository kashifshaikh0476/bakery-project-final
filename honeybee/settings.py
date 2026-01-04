import os
from pathlib import Path
# import django_on_heroku  <-- Ye hata diya kyunki ye error de raha tha

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e7y2svjrg+u-1s+$*@u_vkemd=j_%*uvk&+76)_9ii94xip#31'

DEBUG = True
ALLOWED_HOSTS = ['*']

# Isse bina slash (/) ke bhi about page khul jayega
APPEND_SLASH = True 

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    'phone_field',
    'django_google_maps'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Professional CSS ke liye add kiya
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'honeybee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'honeybee.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & Media Settings (Images show hone ke liye)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/order/order'
LOGOUT_REDIRECT_URL = '/'

GOOGLE_MAPS_API_KEY='AIzaSyCgs1hVUNcVzjhRtSA8XJSVBnQcm_yIzqo'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django_on_heroku.settings(locals()) <-- Ye bhi hata diya

JAZZMIN_SETTINGS = {
    "site_title": "A1 Bakery Admin",
    "site_header": "A1 Bakery Manager",
    "site_brand": "A1 Bakery",
    "welcome_sign": "Welcome, Owner!",
    "copyright": "A1 Bakery Ltd",
    "search_model": "main_app.Product",
    "topmenu_links": [
        {"name": "Open Website", "url": "home", "permissions": ["auth.view_user"]},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "main_app.Product": "fas fa-birthday-cake",
        "main_app.Order": "fas fa-shopping-cart",
        "main_app.Feedback": "fas fa-star",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly", 
    "navbar": "navbar-dark", 
    "sidebar": "sidebar-dark-warning",
    "accent": "accent-warning",
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
