"""
Wagtail Page Models for ARC CMS
Defines the content structure for the headless CMS
"""

import logging
from django.db import models
from django.contrib.auth.models import User as AuthUser
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.images.models import Image
from wagtail.images.api.fields import ImageRenditionField
from wagtail import blocks
from modelcluster.fields import ParentalKey

# Import custom blocks with proper API serialization
from .blocks import (
    HeroBlock, AboutBlock, EventBlock, GalleryImageBlock, YouTubeVideoBlock,
    TestimonialBlock, TeamMemberBlock, RuleBlock,
    StatBlock, ValueCardBlock, CompetitionCategoryBlock,
    EventDetailBlock, BenefitCardBlock, RuleCategoryBlock,
    RuleDocumentBlock, OrganizerBlock, OrganizerStatBlock,
    SponsorBlock, ContactInfoBlock, SocialLinkBlock, NavigationItemBlock, CTABlock
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

log = logging.getLogger(__name__)


# ===============================================================================
# Base Page Models
# ===============================================================================

class BasePage(Page):
    """
    Abstract base page with common fields for all pages
    """
    show_in_menus_default = True
    
    class Meta:
        abstract = True


# ===============================================================================
# Home Page
# ===============================================================================

class HomePage(BasePage):
    """
    Main landing page with flexible StreamField content
    """
    template = "cms_app/home_page.html"
    
    # Hero Section
    hero_title = models.CharField(max_length=255, default="Welcome to ARC")
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Flexible Content - Comprehensive blocks for all sections
    body = StreamField([
        # Hero Section
        ('hero', HeroBlock()),
        
        # About Section
        ('about', AboutBlock()),
        ('about_stats', blocks.ListBlock(StatBlock(), label='About Stats (e.g., 5+ Years)')),
        ('value_cards', blocks.ListBlock(ValueCardBlock(), label='Value Cards (Innovation, Community, etc.)')),
        
        # Events Section
        ('event_details', blocks.ListBlock(EventDetailBlock(), label='Event Details (Full Event Cards)')),
        ('events_cta', CTABlock(label='Events Call to Action')),
        
        # Volunteer Section
        ('volunteer_image', GalleryImageBlock(label='Volunteer Section Image')),
        ('volunteer_stats', blocks.ListBlock(StatBlock(), label='Volunteer Stats')),
        ('benefit_cards', blocks.ListBlock(BenefitCardBlock(), label='Volunteer Benefits')),
        ('volunteer_cta', CTABlock(label='Volunteer Call to Action')),
        
        # Gallery Section
        ('gallery', blocks.ListBlock(GalleryImageBlock(), label='Gallery Images')),
        ('youtube_videos', blocks.ListBlock(YouTubeVideoBlock(), label='YouTube Videos')),
        
        # Rules Section
        ('rule_categories', blocks.ListBlock(RuleCategoryBlock(), label='Competition Rule Categories')),
        ('general_rules', blocks.ListBlock(blocks.CharBlock(max_length=255), label='General Rules List')),
        ('rule_documents', blocks.ListBlock(RuleDocumentBlock(), label='Rule Documents for Download')),
        ('rules_faq_cta', CTABlock(label='Rules FAQ Call to Action')),
        
        # Organizers Section
        ('organizers', blocks.ListBlock(OrganizerBlock(), label='Organizers/Partners')),
        ('organizer_stats', blocks.ListBlock(OrganizerStatBlock(), label='Organizer Impact Stats')),
        ('organizers_cta', CTABlock(label='Organizers Network CTA')),
        
        # Generic Content
        ('testimonials', blocks.ListBlock(TestimonialBlock(), label='Testimonials')),
        ('team', blocks.ListBlock(TeamMemberBlock(), label='Team Members')),
        ('rules', blocks.ListBlock(RuleBlock(), label='Simple Rules')),
        ('events', blocks.ListBlock(EventBlock(), label='Simple Events')),
        ('cta', CTABlock(label='Call to Action')),
        ('rich_text', blocks.RichTextBlock(label='Rich Text Content')),
        ('html', blocks.RawHTMLBlock(label='Raw HTML')),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_background'),
        ], heading="Hero Section"),
        FieldPanel('body'),
    ]
    
    # API Configuration
    api_fields = [
        APIField('hero_title'),
        APIField('hero_subtitle'),
        APIField('hero_background', serializer=ImageRenditionField('fill-1920x1080')),
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "Home Page"


# ===============================================================================
# About Page
# ===============================================================================

class AboutPage(BasePage):
    """
    About page with mission, vision, and team information
    """
    template = "cms_app/about_page.html"
    
    intro = RichTextField(blank=True, help_text="Introduction text")
    mission = RichTextField(blank=True, help_text="Mission statement")
    vision = RichTextField(blank=True, help_text="Vision statement")
    
    body = StreamField([
        ('about', AboutBlock()),
        ('team', blocks.ListBlock(TeamMemberBlock())),
        ('testimonials', blocks.ListBlock(TestimonialBlock())),
        ('rich_text', blocks.RichTextBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('mission'),
        FieldPanel('vision'),
        FieldPanel('body'),
    ]
    
    api_fields = [
        APIField('intro'),
        APIField('mission'),
        APIField('vision'),
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "About Page"


# ===============================================================================
# Events Page
# ===============================================================================

class EventsPage(BasePage):
    """
    Events listing page
    """
    template = "cms_app/events_page.html"
    
    intro = RichTextField(blank=True)
    
    body = StreamField([
        ('events', blocks.ListBlock(EventBlock())),
        ('rich_text', blocks.RichTextBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    api_fields = [
        APIField('intro'),
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "Events Page"


# ===============================================================================
# Gallery Page
# ===============================================================================

class GalleryPage(BasePage):
    """
    Image gallery page
    """
    template = "cms_app/gallery_page.html"
    
    intro = RichTextField(blank=True)
    
    body = StreamField([
        ('gallery', blocks.ListBlock(GalleryImageBlock())),
        ('rich_text', blocks.RichTextBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    api_fields = [
        APIField('intro'),
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "Gallery Page"


# ===============================================================================
# Volunteer/Registration Page
# ===============================================================================

class VolunteerPage(BasePage):
    """
    Volunteer registration and information page
    """
    template = "cms_app/volunteer_page.html"
    
    intro = RichTextField(blank=True, help_text="Introduction to volunteering")
    requirements = RichTextField(blank=True, help_text="Volunteer requirements")
    registration_form_url = models.URLField(
        blank=True,
        help_text="External registration form URL"
    )
    
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('testimonials', blocks.ListBlock(TestimonialBlock())),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('requirements'),
        FieldPanel('registration_form_url'),
        FieldPanel('body'),
    ]
    
    api_fields = [
        APIField('intro'),
        APIField('requirements'),
        APIField('registration_form_url'),
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "Volunteer Page"


# ===============================================================================
# Rules Page
# ===============================================================================

class RulesPage(BasePage):
    """
    Rules and guidelines page
    """
    template = "cms_app/rules_page.html"
    
    intro = RichTextField(blank=True)
    
    body = StreamField([
        ('rules', blocks.ListBlock(RuleBlock())),
        ('rich_text', blocks.RichTextBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    api_fields = [
        APIField('intro'),
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "Rules Page"


# ===============================================================================
# Generic/Flexible Page
# ===============================================================================

class FlexiblePage(BasePage):
    """
    Flexible page for any content type
    """
    template = "cms_app/flexible_page.html"
    
    body = StreamField([
        ('hero', HeroBlock()),
        ('about', AboutBlock()),
        ('events', blocks.ListBlock(EventBlock())),
        ('gallery', blocks.ListBlock(GalleryImageBlock())),
        ('testimonials', blocks.ListBlock(TestimonialBlock())),
        ('team', blocks.ListBlock(TeamMemberBlock())),
        ('rules', blocks.ListBlock(RuleBlock())),
        ('rich_text', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
    ], use_json_field=True)
    
    content_panels = BasePage.content_panels + [
        FieldPanel('body'),
    ]
    
    api_fields = [
        APIField('body'),
    ]
    
    class Meta:
        verbose_name = "Flexible Page"


# ===============================================================================
# Site Settings - Global Content (Footer, Contact, Sponsors, etc.)
# ===============================================================================

@register_setting
class SiteSettings(BaseSiteSetting):
    """
    Global site settings for footer, contact info, sponsors, social links, etc.
    Accessible site-wide via the Wagtail API
    """
    
    class Meta:
        verbose_name = "Site Settings"
    
    # Site Information
    site_name = models.CharField(max_length=255, default="ARC Lebanon")
    site_tagline = models.CharField(max_length=255, blank=True, help_text="Short tagline for the site")
    site_description = models.TextField(blank=True, help_text="Site description for footer")
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Contact Information
    contact_info = StreamField([
        ('contact', ContactInfoBlock()),
    ], use_json_field=True, blank=True)
    
    # Sponsors
    sponsors = StreamField([
        ('sponsor', SponsorBlock()),
    ], use_json_field=True, blank=True)
    
    # Organizers
    organizers = StreamField([
        ('organizer', OrganizerBlock()),
    ], use_json_field=True, blank=True, help_text="Organizers/Partners displayed in footer")
    
    # Social Links
    social_links = StreamField([
        ('social_link', SocialLinkBlock()),
    ], use_json_field=True, blank=True)
    
    # Footer Text
    copyright_text = models.CharField(
        max_length=255,
        default="© 2025 ARC Lebanon. All rights reserved.",
        help_text="Copyright text for footer"
    )
    footer_about_text = models.TextField(blank=True, help_text="About text displayed in footer")
    
    # Navigation Settings
    navigation_items = StreamField([
        ('nav_item', NavigationItemBlock()),
    ], use_json_field=True, blank=True, help_text="Navigation menu items")
    show_login_button = models.BooleanField(default=True, help_text="Show login/register button in navigation")
    login_button_text = models.CharField(max_length=100, default="Login / Register")
    login_url = models.URLField(blank=True, help_text="URL for login page")
    
    # API Configuration for proper image serialization
    api_fields = [
        APIField('site_name'),
        APIField('site_tagline'),
        APIField('site_description'),
        APIField('site_logo', serializer=ImageRenditionField('fill-1920x1080')),
        APIField('contact_info'),
        APIField('sponsors'),
        APIField('organizers'),
        APIField('social_links'),
        APIField('copyright_text'),
        APIField('footer_about_text'),
        APIField('navigation_items'),
        APIField('show_login_button'),
        APIField('login_button_text'),
        APIField('login_url'),
    ]
    
    panels = [
        MultiFieldPanel([
            FieldPanel('site_name'),
            FieldPanel('site_tagline'),
            FieldPanel('site_description'),
            FieldPanel('site_logo'),
        ], heading="Site Information"),
        
        MultiFieldPanel([
            FieldPanel('contact_info'),
        ], heading="Contact Information"),
        
        MultiFieldPanel([
            FieldPanel('sponsors'),
        ], heading="Sponsors"),
        
        MultiFieldPanel([
            FieldPanel('organizers'),
        ], heading="Organizers/Partners"),
        
        MultiFieldPanel([
            FieldPanel('social_links'),
        ], heading="Social Links"),
        
        MultiFieldPanel([
            FieldPanel('copyright_text'),
            FieldPanel('footer_about_text'),
        ], heading="Footer Content"),
        
        MultiFieldPanel([
            FieldPanel('navigation_items'),
            FieldPanel('show_login_button'),
            FieldPanel('login_button_text'),
            FieldPanel('login_url'),
        ], heading="Navigation Settings"),
    ]

