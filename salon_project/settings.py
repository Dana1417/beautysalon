from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# 🚨 Security
# ==========================================================

SECRET_KEY = 'django-insecure-a$%g6^fy$ix(d_j*l+ie!5!u$2j4(lp)zi437ssj-c6tj=j5(u'
DEBUG = True
ALLOWED_HOSTS = []


# ==========================================================
# 🧩 Application definition
# ==========================================================

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ============================
    # 💄 Salon Project Apps
    # ============================
    'accounts',
    'catalog',
    'scheduling',
    'bookings',
    'billing',
    'notifications_center',
    'portal_client',
    'control_panel',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # لدعم اللغة العربية والـ RTL
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'salon_project.urls'


# ==========================================================
# 🎨 Templates
# ==========================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'salon_project.wsgi.application'


# ==========================================================
# 🗄 Database
# ==========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================================
# 🔐 Password validation
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================================
# 🌍 Internationalization
# ==========================================================

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True
USE_TZ = True


# ==========================================================
# 🎨 Static Files (CSS - JS - Images)
# ==========================================================

STATIC_URL = '/static/'

# مكان مجلد static داخل مشروعك
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# مكان جمع الملفات عند التحزيم (production)
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ==========================================================
# 🖼 Media Files (User uploads)
# ==========================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================================
# 🔑 Default PK type + Custom User Model
# ==========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'
