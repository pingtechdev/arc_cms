"""
Management command to populate the CMS with test data for frontend testing
"""

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from wagtail.images.models import Image
from cms_app.models import HomePage, SiteSettings
from django.core.files.images import ImageFile
import os


class Command(BaseCommand):
    help = 'Populates CMS with test data for complete frontend testing'

    def handle(self, *args, **options):
        self.stdout.write('Starting CMS test data population...')
        
        # Get existing HomePage or use the first one
        try:
            home_page = HomePage.objects.first()
            if not home_page:
                raise HomePage.DoesNotExist
            self.stdout.write(f'Found existing HomePage: {home_page.title}')
        except (HomePage.DoesNotExist, AttributeError):
            self.stdout.write(self.style.ERROR('No HomePage found! Please create one first.'))
            return
        
        # Update HomePage with comprehensive content
        home_page.body = [
            # Hero Section - 3 slides
            ('hero', {
                'title': 'Welcome to ARC 2025',
                'subtitle': 'Annual Robotics Competition',
                'description': '<p>Join us for the most exciting robotics competition in Lebanon!</p>',
                'cta_text': 'Register Now',
                'cta_link': '#events',
                'secondary_cta_text': 'Become a Volunteer',
                'secondary_cta_link': '#volunteers',
            }),
            ('hero', {
                'title': 'Innovate. Compete. Excel.',
                'subtitle': 'Push the Boundaries of Robotics',
                'description': '<p>Challenge yourself and showcase your robotics skills.</p>',
                'cta_text': 'View Events',
                'cta_link': '#events',
                'secondary_cta_text': 'Learn More',
                'secondary_cta_link': '#about',
            }),
            ('hero', {
                'title': 'Join the Future of Robotics',
                'subtitle': 'Innovation Meets Excellence',
                'description': '<p>Be part of Lebanon\'s premier robotics community.</p>',
                'cta_text': 'Get Started',
                'cta_link': '#events',
                'secondary_cta_text': 'View Gallery',
                'secondary_cta_link': '#gallery',
            }),
            
            # About Section
            ('about_stats', [
                {'number': '5+', 'label': 'Years Active'},
                {'number': '1000+', 'label': 'Participants'},
            ]),
            ('value_cards', [
                {
                    'icon_name': 'Target',
                    'title': 'Innovation',
                    'description': 'Pushing boundaries with cutting-edge robotics technology and creative problem-solving.'
                },
                {
                    'icon_name': 'Users',
                    'title': 'Community',
                    'description': 'Building a supportive network of robotics enthusiasts, mentors, and innovators.'
                },
                {
                    'icon_name': 'Trophy',
                    'title': 'Excellence',
                    'description': 'Striving for the highest standards in competition and technical achievement.'
                },
                {
                    'icon_name': 'Lightbulb',
                    'title': 'Learning',
                    'description': 'Continuous education and skill development in robotics and STEM fields.'
                },
            ]),
            
            # Events Section
            ('event_details', [
                {
                    'title': 'ARC Championship 2025',
                    'date': 'March 15-17, 2025',
                    'time': '9:00 AM - 6:00 PM',
                    'location': 'American University of Beirut',
                    'participants': '100+ Teams',
                    'description': 'The main robotics championship featuring multiple competition categories.',
                    'status': 'Registration Open',
                    'status_color': 'bg-secondary',
                    'button_text': 'Learn More',
                },
                {
                    'title': 'Robotics Workshop',
                    'date': 'February 20, 2025',
                    'time': '10:00 AM - 4:00 PM',
                    'location': 'Lebanese American University',
                    'participants': '50+ Participants',
                    'description': 'Hands-on workshop covering robot design, programming, and competition strategies.',
                    'status': 'Coming Soon',
                    'status_color': 'bg-accent',
                    'button_text': 'Learn More',
                },
                {
                    'title': 'Junior Challenge',
                    'date': 'April 10, 2025',
                    'time': '9:00 AM - 3:00 PM',
                    'location': 'Université Saint-Joseph',
                    'participants': '60+ Young Engineers',
                    'description': 'Special competition category for students aged 12-16.',
                    'status': 'Registration Opens Soon',
                    'status_color': 'bg-muted',
                    'button_text': 'Learn More',
                },
            ]),
            ('events_cta', {
                'title': "Don't Miss Out!",
                'description': 'Subscribe to our newsletter for the latest updates, event announcements, and exclusive content.',
                'primary_button_text': 'Subscribe Now',
                'background_style': 'gradient',
            }),
            
            # Volunteer Section
            ('volunteer_stats', [
                {'number': '200+', 'label': 'Active Volunteers'},
                {'number': '5+', 'label': 'Years Running'},
            ]),
            ('benefit_cards', [
                {
                    'icon_name': 'Users',
                    'title': 'Community Impact',
                    'description': 'Make a difference by supporting STEM education and inspiring young innovators.'
                },
                {
                    'icon_name': 'Heart',
                    'title': 'Meaningful Experience',
                    'description': 'Gain valuable experience while contributing to a cause you believe in.'
                },
                {
                    'icon_name': 'Star',
                    'title': 'Skill Development',
                    'description': 'Develop leadership, teamwork, and technical skills through hands-on involvement.'
                },
            ]),
            ('volunteer_cta', {
                'title': 'Ready to Make a Difference?',
                'description': 'Join our team of dedicated volunteers and help shape the future of robotics education.',
                'primary_button_text': 'Join Now',
                'background_style': 'gradient',
            }),
            
            # Rules Section
            ('rule_categories', [
                {
                    'icon_name': 'Trophy',
                    'title': 'Autonomous Navigation',
                    'description': 'Robots must navigate through obstacles autonomously without human intervention.',
                    'rules': [
                        'Maximum robot size: 30x30x30 cm',
                        'Autonomous operation only',
                        'Time limit: 5 minutes',
                    ]
                },
                {
                    'icon_name': 'Users',
                    'title': 'Robot Soccer',
                    'description': 'Teams of robots compete in an exciting soccer match.',
                    'rules': [
                        'Team size: 3-5 robots',
                        'Match duration: 2x5 minutes',
                        'Ball detection required',
                    ]
                },
                {
                    'icon_name': 'Settings',
                    'title': 'Line Following',
                    'description': 'Robots follow a black line on white surface at maximum speed.',
                    'rules': [
                        'Single robot per team',
                        'Must follow black line',
                        'Speed and accuracy both count',
                    ]
                },
                {
                    'icon_name': 'Shield',
                    'title': 'Sumo Wrestling',
                    'description': 'Robots push each other out of a circular ring.',
                    'rules': [
                        'Weight limit: 3 kg',
                        'Ring diameter: 154 cm',
                        'Best of 3 matches',
                    ]
                },
            ]),
            ('general_rules', [
                'All teams must register by the deadline',
                'Robots must pass safety inspection before competing',
                'Teams can participate in multiple categories',
                'Fair play and sportsmanship are mandatory',
                'Protests must be filed within 15 minutes',
                "Judges' decisions are final",
            ]),
            ('rule_documents', [
                {
                    'name': 'Complete Rule Book 2025',
                    'file_type': 'PDF',
                    'file_size': '2.1 MB',
                },
                {
                    'name': 'Safety Guidelines',
                    'file_type': 'PDF',
                    'file_size': '1.5 MB',
                },
                {
                    'name': 'Registration Form',
                    'file_type': 'PDF',
                    'file_size': '856 KB',
                },
                {
                    'name': 'Technical Specifications',
                    'file_type': 'PDF',
                    'file_size': '3.2 MB',
                },
            ]),
            ('rules_faq_cta', {
                'title': 'Have Questions?',
                'description': 'Check our FAQ or contact our technical support team for clarification on any rules.',
                'primary_button_text': 'View FAQ',
                'secondary_button_text': 'Contact Technical Support',
                'background_style': 'gradient',
            }),
            
            # Organizers Section
            ('organizers', [
                {
                    'name': 'Kalimat',
                    'description': 'Leading educational technology company supporting robotics education',
                    'role': 'Main Sponsor',
                },
                {
                    'name': 'Teachers Association',
                    'description': 'Professional organization of educators promoting STEM education',
                    'role': 'Educational Partner',
                },
                {
                    'name': 'Technical Committee',
                    'description': 'Expert panel ensuring fair competition and technical excellence',
                    'role': 'Technical Oversight',
                },
                {
                    'name': 'University Partners',
                    'description': 'Academic institutions providing venue and technical support',
                    'role': 'Academic Partners',
                },
            ]),
            ('organizer_stats', [
                {'icon_name': 'Building2', 'number': '15+', 'label': 'Partner Organizations'},
                {'icon_name': 'Users', 'number': '50+', 'label': 'Expert Volunteers'},
                {'icon_name': 'Award', 'number': '5+', 'label': 'Years Experience'},
                {'icon_name': 'Globe', 'number': '3', 'label': 'Countries Represented'},
            ]),
            ('organizers_cta', {
                'title': 'Join Our Network',
                'description': 'Are you an organization passionate about robotics education? We\'re always looking for new partners to help us expand our impact.',
                'primary_button_text': 'Become a Partner',
                'secondary_button_text': 'Learn More',
                'background_style': 'gradient',
            }),
        ]
        
        home_page.save()
        revision = home_page.save_revision()
        revision.publish()
        
        self.stdout.write(self.style.SUCCESS('[OK] HomePage content populated'))
        
        # Update Site Settings
        try:
            site = Site.objects.get(is_default_site=True)
            settings = SiteSettings.for_site(site)
            
            settings.site_name = "ARC Lebanon"
            settings.site_tagline = "Annual Robotics Competition"
            settings.site_description = "Empowering the next generation of robotics innovators through competition, education, and community building."
            settings.copyright_text = "(c) 2025 ARC Lebanon. All rights reserved."
            settings.footer_about_text = "ARC Lebanon is the premier robotics competition in the region, bringing together students, educators, and technology enthusiasts."
            settings.login_button_text = "Login / Register"
            
            # Contact Info
            settings.contact_info = [
                ('contact', {'icon_name': 'MapPin', 'label': 'Location', 'value': 'Beirut, Lebanon'}),
                ('contact', {'icon_name': 'Phone', 'label': 'Phone', 'value': '+961 1 234 567'}),
                ('contact', {'icon_name': 'Mail', 'label': 'Email', 'value': 'info@arc-robotics.com'}),
                ('contact', {'icon_name': 'Globe', 'label': 'Website', 'value': 'www.arc-robotics.com'}),
            ]
            
            # Social Links
            settings.social_links = [
                ('social_link', {'name': 'LinkedIn', 'url': 'https://linkedin.com/company/arc-lebanon', 'icon_name': 'Linkedin'}),
                ('social_link', {'name': 'Twitter', 'url': 'https://twitter.com/arc_lebanon', 'icon_name': 'Twitter'}),
                ('social_link', {'name': 'Instagram', 'url': 'https://instagram.com/arc_lebanon', 'icon_name': 'Instagram'}),
            ]
            
            # Note: Sponsors would be added with actual logos
            # For now, we'll add placeholder sponsor names
            settings.sponsors = [
                ('sponsor', {'name': 'Sponsor 1'}),
                ('sponsor', {'name': 'Sponsor 2'}),
                ('sponsor', {'name': 'Sponsor 3'}),
                ('sponsor', {'name': 'Sponsor 4'}),
            ]
            
            settings.save()
            self.stdout.write(self.style.SUCCESS('[OK] Site Settings populated'))
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not update Site Settings: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] CMS test data population complete!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('  1. Access CMS admin at: http://localhost:8000/cms/')
        self.stdout.write('  2. View API at: http://localhost:8000/api/v2/pages/?type=cms_app.HomePage')
        self.stdout.write('  3. Test the frontend integration')

