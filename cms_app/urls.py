"""
URL Configuration for CMS App API
"""
from django.urls import path, include
from .api import api_router, SiteSettingsAPIView

urlpatterns = [
    path('api/v2/', api_router.urls),
    path('api/v2/settings/', SiteSettingsAPIView.as_view(), name='site-settings'),
]

