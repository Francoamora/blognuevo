import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Base del proyecto. Uso Path para evitar líos de rutas entre SO.
BASE_DIR = Path(__file__).resolve().parent.parent

# La SECRET_KEY real vive en variables de entorno en prod.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'morita_23')

# Producción por defecto; en local exporto DJANGO_DEBUG=True
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# Hosts válidos (local + PythonAnywhere).
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'francomora23.pythonanywhere.com',
    'www.francomora23.pythonanywhere.com',
    '.pythonanywhere.com',
]

# CSRF confiables: evito rechazos en HTTPS.
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://francomora23.pythonanywhere.com',
    'https://www.francomora23.pythonanywhere.com',
]

# Core + ckeditor/uploader y mi app.
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

# Middleware estándar.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

# Templates: uso carpeta /templates a nivel proyecto + las de cada app.
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

WSGI_APPLICATION = 'blog.wsgi.application'

# Para este proyecto alcanza sqlite (también en PA).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Validaciones mínimas (acorde al alcance del proyecto).
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# Español AR y TZ local.
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Static: en dev desde /static, en PA recolecto a /staticfiles.
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = '/home/Francomora23/blognuevo/staticfiles'

# Media: separo rutas entre dev y prod.
MEDIA_URL = '/media/'
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_ROOT = '/home/Francomora23/blognuevo/media'

# En prod activo nombres con hash para cache-busting automático.
if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# CKEditor: configuración básica + uploader activo.
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join(['uploadimage']),
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
    },
}

# Flujo de login/logout simple.
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'

# Mensajes → clases de Bootstrap.
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email: en prod levanto credenciales por env. En local dejo defaults para test.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'elblogdevideojuegos2025@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'rtqc qwpb wfzb hijf')  # en prod: siempre por env
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = 'Blog de Videojuegos <elblogdevideojuegos2025@gmail.com>'
