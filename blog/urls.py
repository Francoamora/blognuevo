from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App1.urls')),  # Se incluye todo lo de App1
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Servir media solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
