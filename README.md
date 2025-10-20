# ARC CMS - Wagtail Headless CMS

A headless Wagtail CMS backend for the ARC Lebanon website.

## 🚀 Features

- **Wagtail CMS** - Modern Django-based CMS
- **Headless API** - RESTful API for frontend consumption
- **Custom Models** - HomePage, AboutPage, EventsPage, etc.
- **Media Management** - Image and document handling
- **Site Settings** - Global site configuration

## 🛠️ Tech Stack

- **Django 5.2+** - Web framework
- **Wagtail 7.1+** - CMS framework
- **MySQL** - Database
- **Gunicorn** - WSGI server
- **Nginx** - Web server

## 📁 Project Structure

```
arc_cms/
├── cms_core/           # Django project settings
│   ├── settings.py     # Main settings
│   ├── local_settings.py # Production settings
│   └── urls.py         # URL configuration
├── cms_app/           # Main application
│   ├── models.py       # Page models
│   ├── api.py          # API endpoints
│   ├── blocks.py       # StreamField blocks
│   └── templates/      # Page templates
├── media/             # User uploaded files
├── staticfiles/       # Collected static files
├── requirements.txt    # Python dependencies
└── manage.py         # Django management
```

## 🔧 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database:**
   - Update `cms_core/local_settings.py` with your database credentials

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

## 🌐 API Endpoints

- **Pages API:** `/api/v2/pages/`
- **Images API:** `/api/v2/images/`
- **Documents API:** `/api/v2/documents/`
- **Site Settings:** `/api/v2/settings/`
- **Wagtail Admin:** `/cms/`

## 🚀 Deployment

The project is configured for production deployment with:
- Gunicorn WSGI server
- Nginx reverse proxy
- MySQL database
- Static/media file serving

## 📝 Environment Variables

Configure in `cms_core/local_settings.py`:
- Database credentials
- Media/static file paths
- Allowed hosts
- CORS settings