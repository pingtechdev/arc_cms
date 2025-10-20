"""
URL configuration for Wagtail CMS project.
"""
from cms_core import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from cms_app.api import SiteSettingsAPIView

# Create API router
api_router = WagtailAPIRouter('wagtailapi')

# Register API endpoints
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

urlpatterns = [
    # Django Admin (for database management)
    path('django-admin/', admin.site.urls),

    # Wagtail CMS Admin
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # Wagtail API (for headless CMS)
    path('api/v2/', api_router.urls),
    
    # Custom API endpoints
    path('api/v2/settings/', SiteSettingsAPIView.as_view()),
    
    # Custom app URLs
    path('', include('cms_app.urls')),
]

# Serve media and static files in development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve Wagtail pages (catch-all at the end)
urlpatterns += [
    re_path(r'', include(wagtail_urls)),
]
