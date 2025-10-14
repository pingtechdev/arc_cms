"""
Management command to fix Wagtail page tree structure
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site


class Command(BaseCommand):
    help = 'Fix Wagtail page tree structure'

    def handle(self, *args, **options):
        self.stdout.write('Fixing Wagtail page tree...')
        
        # Get or create root page
        try:
            root = Page.objects.get(depth=1)
            self.stdout.write(f'Root page found: {root}')
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR('Root page not found! Creating...'))
            root = Page.add_root(
                title="Root",
                slug="root",
                content_type_id=1,
                depth=1,
                path='0001',
            )
            self.stdout.write(self.style.SUCCESS('Root page created'))
        
        # Fix the tree
        self.stdout.write('Fixing tree structure...')
        Page.fix_tree()
        self.stdout.write(self.style.SUCCESS('Tree structure fixed!'))
        
        # Check for existing HomePage
        from cms_app.models import HomePage
        home_pages = HomePage.objects.all()
        
        if home_pages.exists():
            self.stdout.write(f'Found {home_pages.count()} HomePage(s)')
            for hp in home_pages:
                self.stdout.write(f'  - {hp.title} (ID: {hp.id})')
        else:
            self.stdout.write('No HomePage found yet - you can create one in the admin')
        
        # Update site if needed
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            self.stdout.write(f'Default site: {site.site_name} -> {site.root_page}')
            
            # If there's a HomePage, set it as root
            if home_pages.exists():
                home = home_pages.first()
                if site.root_page != home:
                    site.root_page = home
                    site.save()
                    self.stdout.write(self.style.SUCCESS(f'Site root updated to: {home.title}'))
        
        self.stdout.write(self.style.SUCCESS('\nTree fixed! You can now create pages in the admin.'))

