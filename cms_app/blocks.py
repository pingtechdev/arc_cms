"""
Custom StreamField blocks with proper API serialization
"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.api.fields import ImageRenditionField


class APIImageChooserBlock(ImageChooserBlock):
    """ImageChooserBlock that returns full image data in API"""
    
    def get_api_representation(self, value, context=None):
        if value:
            # Get the request from context to build full URLs
            request = context.get('request') if context else None
            base_url = ''
            if request:
                base_url = f"{request.scheme}://{request.get_host()}"
            
            return {
                'id': value.id,
                'title': value.title,
                'original': base_url + value.file.url,
                'width': value.width,
                'height': value.height,
                'thumbnail': base_url + value.get_rendition('max-500x500').url if value else None,
                'large': base_url + value.get_rendition('max-1920x1080').url if value else None,
            }
        return None


class HeroBlock(blocks.StructBlock):
    """Hero section with image, title, and CTA"""
    title = blocks.CharBlock(max_length=255, help_text="Main heading")
    subtitle = blocks.CharBlock(max_length=255, required=False, help_text="Subheading text")
    description = blocks.RichTextBlock(required=False, help_text="Hero description")
    background_image = APIImageChooserBlock(required=False, help_text="Background image")
    
    # Primary CTA (Red button)
    cta_text = blocks.CharBlock(max_length=100, required=False, help_text="Primary button text (e.g., 'Register Now')")
    cta_link = blocks.URLBlock(required=False, help_text="Primary button link")
    
    # Secondary CTA (Outlined button)
    secondary_cta_text = blocks.CharBlock(max_length=100, required=False, help_text="Secondary button text (e.g., 'Become a Volunteer')")
    secondary_cta_link = blocks.URLBlock(required=False, help_text="Secondary button link")
    
    class Meta:
        template = 'cms_app/blocks/hero_block.html'
        icon = 'image'
        label = 'Hero Section'


class AboutBlock(blocks.StructBlock):
    """About section with rich content"""
    title = blocks.CharBlock(max_length=255, help_text="Section title")
    content = blocks.RichTextBlock(help_text="About content")
    image = APIImageChooserBlock(required=False, help_text="Optional image")
    
    class Meta:
        template = 'cms_app/blocks/about_block.html'
        icon = 'doc-full'
        label = 'About Section'


class EventBlock(blocks.StructBlock):
    """Single event block"""
    title = blocks.CharBlock(max_length=255)
    date = blocks.DateBlock(required=False)
    time = blocks.TimeBlock(required=False)
    location = blocks.CharBlock(max_length=255, required=False)
    description = blocks.RichTextBlock(required=False)
    image = APIImageChooserBlock(required=False)
    registration_link = blocks.URLBlock(required=False, help_text="Event registration URL")
    
    class Meta:
        template = 'cms_app/blocks/event_block.html'
        icon = 'date'
        label = 'Event'


class GalleryImageBlock(blocks.StructBlock):
    """Single gallery image"""
    image = APIImageChooserBlock()
    caption = blocks.CharBlock(max_length=255, required=False)
    
    class Meta:
        template = 'cms_app/blocks/gallery_image_block.html'
        icon = 'image'
        label = 'Gallery Image'


class YouTubeVideoBlock(blocks.StructBlock):
    """YouTube video block for gallery"""
    title = blocks.CharBlock(max_length=255, help_text="Video title")
    youtube_url = blocks.URLBlock(help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)")
    thumbnail = APIImageChooserBlock(required=False, help_text="Custom thumbnail (optional)")
    description = blocks.TextBlock(required=False, help_text="Video description")
    
    class Meta:
        template = 'cms_app/blocks/youtube_video_block.html'
        icon = 'media'
        label = 'YouTube Video'


class TestimonialBlock(blocks.StructBlock):
    """Testimonial or quote block"""
    quote = blocks.TextBlock(help_text="Testimonial text")
    author = blocks.CharBlock(max_length=100)
    role = blocks.CharBlock(max_length=150, required=False)
    avatar = APIImageChooserBlock(required=False)
    
    class Meta:
        template = 'cms_app/blocks/testimonial_block.html'
        icon = 'openquote'
        label = 'Testimonial'


class TeamMemberBlock(blocks.StructBlock):
    """Team member or organizer block"""
    name = blocks.CharBlock(max_length=100)
    role = blocks.CharBlock(max_length=150)
    bio = blocks.TextBlock(required=False)
    photo = APIImageChooserBlock(required=False)
    email = blocks.EmailBlock(required=False)
    phone = blocks.CharBlock(max_length=50, required=False)
    
    class Meta:
        template = 'cms_app/blocks/team_member_block.html'
        icon = 'user'
        label = 'Team Member'


class RuleBlock(blocks.StructBlock):
    """Rule or guideline block"""
    rule_number = blocks.CharBlock(max_length=10, required=False)
    title = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock()
    
    class Meta:
        template = 'cms_app/blocks/rule_block.html'
        icon = 'list-ol'
        label = 'Rule'


# ===================================================
# About Section Blocks
# ===================================================

class StatBlock(blocks.StructBlock):
    """Stat display block (e.g., 5+ Years)"""
    number = blocks.CharBlock(max_length=50, help_text="Stat value (e.g., '5+', '1000+')")
    label = blocks.CharBlock(max_length=100, help_text="Stat label (e.g., 'Years Active', 'Participants')")
    
    class Meta:
        icon = 'list-ul'
        label = 'Stat'


class ValueCardBlock(blocks.StructBlock):
    """Value card for About section (Innovation, Community, etc.)"""
    icon_name = blocks.CharBlock(max_length=50, help_text="Lucide icon name (e.g., 'Target', 'Users', 'Trophy', 'Lightbulb')")
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    
    class Meta:
        icon = 'tick-inverse'
        label = 'Value Card'


class CompetitionCategoryBlock(blocks.StructBlock):
    """Competition category block"""
    name = blocks.CharBlock(max_length=100)
    
    class Meta:
        icon = 'list-ul'
        label = 'Competition Category'


# ===================================================
# Events Section Blocks
# ===================================================

class EventDetailBlock(blocks.StructBlock):
    """Detailed event block for Events section"""
    title = blocks.CharBlock(max_length=255)
    date = blocks.CharBlock(max_length=100, help_text="Event date")
    time = blocks.CharBlock(max_length=100, help_text="Event time")
    location = blocks.CharBlock(max_length=255)
    participants = blocks.CharBlock(max_length=100, help_text="e.g., '100+ Teams'")
    description = blocks.TextBlock()
    status = blocks.CharBlock(max_length=50, help_text="e.g., 'Registration Open', 'Coming Soon'")
    status_color = blocks.ChoiceBlock(choices=[
        ('bg-secondary', 'Secondary (Red)'),
        ('bg-accent', 'Accent (Blue)'),
        ('bg-muted', 'Muted (Gray)'),
    ], default='bg-secondary')
    button_text = blocks.CharBlock(max_length=50, default="Learn More")
    button_link = blocks.URLBlock(required=False)
    image = APIImageChooserBlock(required=False)
    
    class Meta:
        icon = 'date'
        label = 'Event Detail'


# ===================================================
# Volunteer Section Blocks
# ===================================================

class BenefitCardBlock(blocks.StructBlock):
    """Benefit card for Volunteer section"""
    icon_name = blocks.CharBlock(max_length=50, help_text="Lucide icon name (e.g., 'Users', 'Heart', 'Star')")
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    
    class Meta:
        icon = 'pick'
        label = 'Benefit Card'


# ===================================================
# Rules Section Blocks
# ===================================================

class RuleCategoryBlock(blocks.StructBlock):
    """Detailed rule category block"""
    icon_name = blocks.CharBlock(max_length=50, help_text="Lucide icon name (e.g., 'Trophy', 'Users', 'Settings', 'Shield')")
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    rules = blocks.ListBlock(blocks.CharBlock(max_length=255, label="Rule"))
    
    class Meta:
        icon = 'list-ul'
        label = 'Rule Category'


class RuleDocumentBlock(blocks.StructBlock):
    """Document download block - supports any file type with caption/description"""
    name = blocks.CharBlock(max_length=255, help_text="Display name for the document")
    document = DocumentChooserBlock(required=True, help_text="Upload any file type (PDF, DOC, XLS, etc.)")
    description = blocks.TextBlock(required=False, help_text="Optional description or caption for the document")
    file_type = blocks.CharBlock(max_length=20, required=False, help_text="File type (auto-detected from upload)")
    file_size = blocks.CharBlock(max_length=20, required=False, help_text="File size (auto-calculated)")
    
    class Meta:
        icon = 'doc-full'
        label = 'Document'


# ===================================================
# Organizers Section Blocks
# ===================================================

class OrganizerBlock(blocks.StructBlock):
    """Organizer/Partner block"""
    name = blocks.CharBlock(max_length=100)
    logo = APIImageChooserBlock(required=False)
    description = blocks.TextBlock()
    role = blocks.CharBlock(max_length=100, help_text="e.g., 'Main Sponsor', 'Educational Partner'")
    
    class Meta:
        icon = 'group'
        label = 'Organizer'


class OrganizerStatBlock(blocks.StructBlock):
    """Organizer impact stat"""
    icon_name = blocks.CharBlock(max_length=50, help_text="Lucide icon name")
    number = blocks.CharBlock(max_length=50)
    label = blocks.CharBlock(max_length=100)
    
    class Meta:
        icon = 'list-ul'
        label = 'Organizer Stat'


# ===================================================
# Footer/Sponsors Section Blocks
# ===================================================

class SponsorBlock(blocks.StructBlock):
    """Sponsor logo block"""
    name = blocks.CharBlock(max_length=100)
    logo = APIImageChooserBlock()
    website = blocks.URLBlock(required=False)
    
    class Meta:
        icon = 'site'
        label = 'Sponsor'


class ContactInfoBlock(blocks.StructBlock):
    """Contact information block"""
    icon_name = blocks.CharBlock(max_length=50, help_text="Lucide icon name (e.g., 'MapPin', 'Phone', 'Mail', 'Globe')")
    label = blocks.CharBlock(max_length=100)
    value = blocks.CharBlock(max_length=255)
    
    class Meta:
        icon = 'mail'
        label = 'Contact Info'


class SocialLinkBlock(blocks.StructBlock):
    """Social media link"""
    name = blocks.CharBlock(max_length=50, help_text="e.g., 'LinkedIn', 'Twitter', 'Instagram'")
    url = blocks.URLBlock()
    icon_name = blocks.CharBlock(max_length=50, required=False, help_text="Lucide icon name (optional)")
    
    class Meta:
        icon = 'site'
        label = 'Social Link'


class NavigationItemBlock(blocks.StructBlock):
    """Navigation menu item"""
    label = blocks.CharBlock(max_length=100, help_text="Menu item label")
    section_id = blocks.CharBlock(max_length=100, help_text="Section ID to scroll to (e.g., 'home', 'about', 'events')")
    order = blocks.IntegerBlock(default=0, help_text="Display order (lower numbers appear first)")
    
    class Meta:
        icon = 'list-ul'
        label = 'Navigation Item'


# ===================================================
# CTA (Call to Action) Blocks
# ===================================================

class CTABlock(blocks.StructBlock):
    """Call-to-action block"""
    title = blocks.CharBlock(max_length=255)
    description = blocks.TextBlock(required=False)
    primary_button_text = blocks.CharBlock(max_length=100)
    primary_button_link = blocks.URLBlock(required=False)
    secondary_button_text = blocks.CharBlock(max_length=100, required=False)
    secondary_button_link = blocks.URLBlock(required=False)
    background_style = blocks.ChoiceBlock(choices=[
        ('gradient', 'Gradient (Red)'),
        ('solid', 'Solid'),
        ('transparent', 'Transparent'),
    ], default='gradient')
    
    class Meta:
        icon = 'pick'
        label = 'Call to Action'

