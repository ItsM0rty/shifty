# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def favicon_view(request):
    """Return a simple favicon response to prevent 400 errors"""
    return HttpResponse(
        content_type="image/svg+xml",
        content='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">☕</text></svg>'
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon_view, name='favicon'),
    path('', include('myapp.urls')),  # ← Includes your app's URLs at the root
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
