# ARC CMS

A Django/Wagtail CMS backend for the ARC project.

## 📁 Project Structure

```
arc_cms/
├── cms_app/               # Main Django app
├── cms_core/              # Django project settings
├── static/                # Static files
├── media/                 # User uploaded files
├── deployment/            # Deployment configuration
│   ├── nginx/             # Nginx configuration
│   ├── systemd/           # Systemd service files
│   ├── config.sh          # Deployment settings
│   ├── deploy.sh          # Deployment script
│   ├── uwsgi.ini          # uWSGI configuration
│   └── README_DEPLOYMENT.md
├── deploy.sh              # Deployment wrapper (calls deployment/deploy.sh)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Development
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Production Deployment
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📖 Documentation

- **Development**: See Django documentation
- **Deployment**: See `deployment/README_DEPLOYMENT.md`

## 🛠️ Technology Stack

- **Django 5.2+** - Web framework
- **Wagtail 5.2+** - CMS
- **MySQL** - Database
- **uWSGI** - Application server
- **Nginx** - Web server