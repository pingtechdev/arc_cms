"""
Wagtail API Configuration for ARC CMS
Provides RESTful API endpoints for headless CMS
"""

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from .models import SiteSettings
from wagtail.models import Site


@method_decorator(never_cache, name='dispatch')
class SiteSettingsAPIView(APIView):
    """
    API endpoint for Site Settings
    """
    
    def get(self, request):
        # Get the default site
        try:
            site = Site.objects.get(is_default_site=True)
            settings = SiteSettings.for_site(site)
            
            # Serialize StreamField blocks manually
            def serialize_streamfield(stream):
                """Convert StreamField to serializable format"""
                if not stream:
                    return []
                
                def serialize_value(value):
                    """Recursively serialize values, handling Image objects"""
                    if hasattr(value, 'file'):  # It's an Image object
                        return {
                            'id': value.id,
                            'title': value.title,
                            'original': request.build_absolute_uri(value.file.url),
                            'width': value.width,
                            'height': value.height,
                            'thumbnail': request.build_absolute_uri(value.get_rendition('max-500x500').url) if value else None,
                            'large': request.build_absolute_uri(value.get_rendition('max-1920x1080').url) if value else None,
                        }
                    elif isinstance(value, dict):
                        return {k: serialize_value(v) for k, v in value.items()}
                    elif isinstance(value, (list, tuple)):
                        return [serialize_value(item) for item in value]
                    else:
                        return value
                
                return [
                    {
                        'type': block.block_type,
                        'value': serialize_value(block.value),
                        'id': str(block.id) if hasattr(block, 'id') else None,
                    }
                    for block in stream
                ]
            
            # Serialize the settings
            data = {
                'site_name': settings.site_name,
                'site_tagline': settings.site_tagline,
                'site_description': settings.site_description,
                'site_logo': {
                    'id': settings.site_logo.id,
                    'title': settings.site_logo.title,
                    'original': request.build_absolute_uri(settings.site_logo.file.url),
                    'width': settings.site_logo.width,
                    'height': settings.site_logo.height,
                    'thumbnail': request.build_absolute_uri(settings.site_logo.get_rendition('max-500x500').url),
                    'large': request.build_absolute_uri(settings.site_logo.get_rendition('max-1920x1080').url),
                } if settings.site_logo else None,
                'contact_info': serialize_streamfield(settings.contact_info),
                'sponsors': serialize_streamfield(settings.sponsors),
                'organizers': serialize_streamfield(settings.organizers),
                'social_links': serialize_streamfield(settings.social_links),
                'copyright_text': settings.copyright_text,
                'footer_about_text': settings.footer_about_text,
                'navigation_items': serialize_streamfield(settings.navigation_items),
                'show_login_button': settings.show_login_button,
                'login_button_text': settings.login_button_text,
                'login_url': settings.login_url,
            }
            
            # Create response with no-cache headers
            response = Response(data)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        except Site.DoesNotExist:
            return Response({'error': 'Default site not found'}, status=404)


# Create the router
api_router = WagtailAPIRouter('wagtailapi')

# Register API endpoints
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

