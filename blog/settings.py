import os
from pathlib import Path
from django.contrib.messages import constants as messages

# 📁 BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SEGURIDAD
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'morita_23')
DEBUG = True
ALLOWED_HOSTS = []

# 📦 APPS INSTALADAS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'App1',
]

# ⚙️ MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌐 URLS PRINCIPALES
ROOT_URLCONF = 'blog.urls'

# 🎨 TEMPLATES
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

# 🔥 WSGI
WSGI_APPLICATION = 'blog.wsgi.application'

# 🗃️ BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# 🌍 INTERNACIONALIZACIÓN
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# 🧾 ARCHIVOS ESTÁTICOS Y MEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✍️ CKEDITOR CONFIG
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',  # tema más claro y moderno
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join(['uploadimage']),
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
    },
}

# 🔐 LOGIN / LOGOUT
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'

# ✅ Etiquetas Bootstrap para mensajes
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# 🆔 PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 📧 CONFIGURACIÓN DE CORREO (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'elblogdevideojuegos2025@gmail.com'  # ⚠️ Usá tu correo real
EMAIL_HOST_PASSWORD = 'rtqc qwpb wfzb hijf'  # ⚠️ Usá contraseña de aplicación si tenés 2FA
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = 'Blog de Videojuegos <elblogdevideojuegos2025@gmail.com>'
