"""
Wagtail hooks for customizing the admin interface
"""

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.utils.html import format_html


@hooks.register('insert_global_admin_css')
def global_admin_css():
    """Add custom CSS to Wagtail admin"""
    return format_html(
        '<style>'
        ':root {{ '
        '--w-color-primary: #dc2626; '
        '--w-color-primary-200: #ef4444; '
        '}}'
        '.w-header {{ background-color: #b91c1c; }}'
        '</style>'
    )


@hooks.register('construct_main_menu')
def configure_main_menu(request, menu_items):
    """Customize the main menu"""
    # You can add custom menu items here
    pass

