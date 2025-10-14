# ARC Standalone Wagtail CMS

A standalone headless CMS built with Django and Wagtail for the ARC project.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Database Setup

Make sure MySQL is running and create the database:

```sql
CREATE DATABASE arc_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Set Up Initial CMS Data

```bash
python manage.py setup_wagtail_cms
```

### 6. Run Server

```bash
python manage.py runserver 0.0.0.0:8001
```

The CMS will be available at:
- **Admin Panel**: http://localhost:8001/cms/
- **API**: http://localhost:8001/api/v2/pages/
- **Django Admin**: http://localhost:8001/django-admin/

## 📚 API Endpoints

- **Pages**: `GET /api/v2/pages/`
- **Page Detail**: `GET /api/v2/pages/{id}/`
- **Images**: `GET /api/v2/images/`
- **Documents**: `GET /api/v2/documents/`

## 🛠️ Management Commands

- `python manage.py setup_wagtail_cms` - Initial setup
- `python manage.py setup_site` - Configure site settings
- `python manage.py fix_wagtail_tree` - Fix page tree structure

## 📝 Configuration

Edit `cms_core/local_settings.py` to configure:
- Database connection
- Media/Static files paths
- CORS settings

## 🔗 Integration

Update your React app to fetch from:
```javascript
const API_BASE = 'http://localhost:8001/api/v2';
```

## 📖 Documentation

- Admin guide available in the main project
- Wagtail docs: https://docs.wagtail.org/

