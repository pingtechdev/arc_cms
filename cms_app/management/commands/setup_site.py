"""
Management command to set up Wagtail site configuration
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from cms_app.models import HomePage


class Command(BaseCommand):
    help = 'Set up Wagtail site configuration'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Wagtail site...')
        
        # Find the HomePage
        home_pages = HomePage.objects.all()
        
        if not home_pages.exists():
            self.stdout.write(self.style.WARNING('No HomePage found. Creating one...'))
            
            # Get root page
            root = Page.objects.get(depth=1)
            
            # Create a default HomePage
            home_page = HomePage(
                title="ARC Home",
                hero_title="Welcome to ARC",
                hero_subtitle="Building a Better Tomorrow",
                slug='home',
                show_in_menus=True,
                draft_title="ARC Home",
            )
            
            root.add_child(instance=home_page)
            revision = home_page.save_revision()
            revision.publish()
            
            self.stdout.write(self.style.SUCCESS(f'Created HomePage: {home_page.title}'))
        else:
            home_page = home_pages.first()
            self.stdout.write(f'Found HomePage: {home_page.title}')
        
        # Set up or update the site
        site = Site.objects.filter(is_default_site=True).first()
        
        if site:
            self.stdout.write(f'Updating existing site: {site.site_name}')
            site.root_page = home_page
            site.site_name = 'ARC CMS'
            site.hostname = 'localhost'
            site.port = 8000
            site.save()
            self.stdout.write(self.style.SUCCESS('Site updated successfully!'))
        else:
            self.stdout.write('Creating new site...')
            Site.objects.create(
                hostname='localhost',
                port=8000,
                root_page=home_page,
                is_default_site=True,
                site_name='ARC CMS'
            )
            self.stdout.write(self.style.SUCCESS('Site created successfully!'))
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Site Configuration Complete!'))
        self.stdout.write('='*60)
        self.stdout.write(f'Site Name: ARC CMS')
        self.stdout.write(f'Hostname: localhost:8000')
        self.stdout.write(f'Root Page: {home_page.title} (ID: {home_page.id})')
        self.stdout.write('\nYour pages are now accessible!')
        self.stdout.write('API: http://localhost:8000/api/v2/pages/')

