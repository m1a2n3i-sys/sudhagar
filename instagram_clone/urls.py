"""
Root URL configuration.
Every incoming request is first checked here. Requests are then
handed off ("included") to the posts app's own urls.py.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin panel
    path('', include('posts.urls')),           # All other URLs handled by posts app
]

# Serve uploaded media files during development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
