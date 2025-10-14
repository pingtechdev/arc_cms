"""
Management command to set up initial Wagtail CMS data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wagtail.models import Page, Site
from cms_app.models import HomePage


class Command(BaseCommand):
    help = 'Set up initial Wagtail CMS data and structure'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Wagtail CMS...')
        
        # Get root page
        root_page = Page.objects.filter(depth=1).first()
        
        if not root_page:
            self.stdout.write(self.style.ERROR('Root page not found!'))
            return
        
        # Check if HomePage already exists
        home_page = HomePage.objects.first()
        
        if not home_page:
            self.stdout.write('Creating initial home page...')
            
            # Delete any existing 'home' pages from default Wagtail installation
            existing_home = Page.objects.filter(slug='home', depth=2).first()
            if existing_home:
                self.stdout.write('Removing default Wagtail home page...')
                existing_home.delete()
                # Refresh root page from database
                root_page = Page.objects.get(id=root_page.id)
            
            # Create HomePage
            home_page = HomePage(
                title="ARC Home",
                hero_title="Welcome to ARC",
                hero_subtitle="Building a Better Tomorrow",
                slug='arc-home',
                show_in_menus=True,
                draft_title="ARC Home",
            )
            
            # Add it as a child of root
            root_page.add_child(instance=home_page)
            revision = home_page.save_revision()
            revision.publish()
            
            self.stdout.write(self.style.SUCCESS(f'Created HomePage: {home_page.title}'))
        else:
            self.stdout.write(f'HomePage already exists: {home_page.title}')
        
        # Set up default site
        site = Site.objects.filter(is_default_site=True).first()
        
        if site:
            if site.root_page != home_page:
                site.root_page = home_page
                site.site_name = 'ARC CMS'
                site.hostname = 'localhost'
                site.port = 8000
                site.save()
                self.stdout.write(self.style.SUCCESS('Updated default site'))
            else:
                self.stdout.write('Default site already configured')
        else:
            Site.objects.create(
                hostname='localhost',
                port=8000,
                root_page=home_page,
                is_default_site=True,
                site_name='ARC CMS'
            )
            self.stdout.write(self.style.SUCCESS('Created default site'))
        
        self.stdout.write(self.style.SUCCESS('\nWagtail CMS setup complete!'))
        self.stdout.write(f'  - Home Page: {home_page.title}')
        self.stdout.write('  - Site configured')
        self.stdout.write('\nNext steps:')
        self.stdout.write('  1. Create a superuser: python manage.py createsuperuser')
        self.stdout.write('  2. Access Wagtail admin at: http://localhost:8000/cms/')
        self.stdout.write('  3. Access Wagtail API at: http://localhost:8000/api/v2/pages/')

