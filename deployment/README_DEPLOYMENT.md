# ARC CMS Backend Deployment Guide

This guide explains how to deploy the ARC CMS (Django/Wagtail) backend application to your Ubuntu server.

## 📁 Project Structure

```
arc_cms/
├── cms_app/                # Django app
├── cms_core/              # Django project settings
├── staticfiles/           # Collected static files (created during deployment)
├── media/                 # User uploaded files
├── logs/                  # Application logs
├── tmp/                   # Temporary files (sockets, PID files)
├── venv/                  # Python virtual environment
├── nginx/                 # Nginx configuration
│   └── arc_cms.conf       # Backend nginx config
├── systemd/               # Systemd service
│   └── arc-cms.service    # Backend service file
├── config.sh              # Deployment configuration
├── deploy.sh              # Deployment script
├── uwsgi.ini              # uWSGI configuration
└── README_DEPLOYMENT.md   # This file
```

## 🚀 Quick Deployment

### 1. Clone and Setup

```bash
# Clone your backend repository
git clone <your-backend-repo> /home/arc_cms
cd /home/arc_cms

# Make deployment script executable
chmod +x deploy.sh
```

### 2. Configure (Optional)

Edit `config.sh` if you need to change any settings:

```bash
# Edit configuration
nano config.sh

# Key settings you might want to change:
# - BACKEND_DOMAIN="api.arc.pingtech.dev"
# - BACKEND_PORT="8001"
# - DB_NAME="arc_cms"
# - DB_USER="arc_user"
# - DB_PASSWORD="arc_secure_password_2024"
```

### 3. Deploy

```bash
# Run deployment
./deploy.sh
```

## 🔧 What the Deployment Does

1. **Checks Requirements**: Python, pip, uWSGI, nginx, MySQL
2. **Creates Directories**: logs, tmp, staticfiles, media
3. **Sets up Virtual Environment**: Python venv with dependencies
4. **Configures Django**: Database settings, static files
5. **Runs Migrations**: Database schema updates
6. **Collects Static Files**: Django collectstatic
7. **Sets up Systemd Service**: Auto-start on boot
8. **Configures Nginx**: Reverse proxy setup
9. **Starts Services**: uWSGI and nginx
10. **Verifies Deployment**: Health checks

## 📊 Configuration Details

### Database Configuration
- **Engine**: MySQL
- **Database**: `arc_cms`
- **User**: `arc_user`
- **Host**: `localhost:3306`

### uWSGI Configuration
- **Port**: 8001 (as requested)
- **Processes**: 4
- **Threads**: 2 per process
- **Socket**: Unix socket for nginx communication

### Nginx Configuration
- **Domain**: `api.arc.pingtech.dev`
- **SSL**: Automatic Let's Encrypt setup
- **Static Files**: Serves Django static files
- **Media Files**: Serves user uploads
- **API Routes**: CORS headers for frontend
- **Admin Panel**: Wagtail admin interface

### Systemd Service
- **Service Name**: `arc-cms`
- **Auto-start**: Enabled on boot
- **User**: `ubuntu`
- **Restart Policy**: Always restart on failure

## 🔄 Updates

To update your backend:

```bash
cd /home/arc_cms
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart arc-cms
```

## 🐛 Troubleshooting

### Common Issues

#### Service Not Starting
```bash
# Check service status
sudo systemctl status arc-cms

# View service logs
sudo journalctl -u arc-cms -f

# Check uWSGI logs
tail -f /var/log/arc/uwsgi.log
```

#### Database Issues
```bash
# Test database connection
cd /home/arc_cms
source venv/bin/activate
python manage.py dbshell

# Check MySQL status
sudo systemctl status mysql
```

#### Static Files Not Loading
```bash
# Collect static files
cd /home/arc_cms
source venv/bin/activate
python manage.py collectstatic --noinput

# Check file permissions
ls -la /home/arc_cms/staticfiles/
```

#### Nginx Issues
```bash
# Test nginx configuration
sudo nginx -t

# Check nginx status
sudo systemctl status nginx

# View nginx logs
sudo tail -f /var/log/nginx/arc_cms_error.log
```

#### Socket Issues
```bash
# Check socket file
ls -la /home/arc_cms/tmp/arc_cms.sock

# Check socket permissions
sudo chown ubuntu:ubuntu /home/arc_cms/tmp/arc_cms.sock
sudo chmod 666 /home/arc_cms/tmp/arc_cms.sock
```

## 📝 Logs

```bash
# Application logs
sudo journalctl -u arc-cms -f
tail -f /var/log/arc/django.log
tail -f /var/log/arc/uwsgi.log

# Nginx logs
sudo tail -f /var/log/nginx/arc_cms_access.log
sudo tail -f /var/log/nginx/arc_cms_error.log

# System logs
sudo journalctl -u nginx -f
```

## 🔧 Management Commands

```bash
# Start/stop/restart service
sudo systemctl start arc-cms
sudo systemctl stop arc-cms
sudo systemctl restart arc-cms

# Check service status
sudo systemctl status arc-cms

# Enable/disable auto-start
sudo systemctl enable arc-cms
sudo systemctl disable arc-cms

# View service logs
sudo journalctl -u arc-cms -f
```

## 🎯 Production Checklist

- [ ] SSL certificates installed
- [ ] Database configured and accessible
- [ ] Django migrations applied
- [ ] Static files collected
- [ ] uWSGI service running
- [ ] Nginx configuration valid
- [ ] Socket file created
- [ ] Admin panel accessible
- [ ] API endpoints responding
- [ ] Health check working

## 📞 Support

For issues:
1. Check service status first
2. View application logs
3. Test database connection
4. Verify nginx configuration
5. Check file permissions

---

**Happy Deploying! 🚀**
