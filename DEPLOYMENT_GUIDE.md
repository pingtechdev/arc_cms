# ARC CMS Deployment Guide

This guide provides step-by-step instructions for deploying the ARC CMS Django application to your VPS under the subdomain `api.arc.pingtech.dev`.

## Prerequisites

- Ubuntu VPS with sudo access
- Python 3.8+ installed
- MySQL/MariaDB installed and running
- Nginx installed and configured
- Git installed
- SSL certificates (Let's Encrypt) configured

## Project Structure

```
/home/ubuntu/projects/arc-deploy/
├── arc_frontend/          # Your existing frontend
└── arc_cms/               # Django CMS backend
    ├── cms_app/
    ├── cms_core/
    ├── manage.py
    ├── requirements.txt
    ├── gunicorn.conf.py
    ├── arc-cms.service
    └── deploy.sh
```

## Step 1: Prepare the VPS Environment

### 1.1 Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install Required System Packages
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y mysql-server mysql-client libmysqlclient-dev
sudo apt install -y nginx git curl
sudo apt install -y build-essential pkg-config
```

### 1.3 Create Project Directory
```bash
mkdir -p /home/ubuntu/projects/arc-deploy
cd /home/ubuntu/projects/arc-deploy
```

## Step 2: Clone and Setup the Project

### 2.1 Clone the Repository
```bash
git clone <your-github-repo-url> arc_cms
cd arc_cms
```

### 2.2 Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn
```

## Step 3: Database Configuration

### 3.1 Setup MySQL Database
```bash
sudo mysql -u root -p
```

In MySQL console, run:
```sql
CREATE DATABASE IF NOT EXISTS arc_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'arc_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON arc_cms.* TO 'arc_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3.2 Update Database Settings
Edit `cms_core/local_settings_production.py` and update the database credentials:
```python
lsettings = {
    'db_name': 'arc_cms',
    'db_user': 'arc_user',
    'db_pass': 'your_actual_secure_password',  # Change this
    'db_host': 'localhost',
    'db_port': '3306',
    # ... rest of settings
}
```

## Step 4: Django Application Setup

### 4.1 Copy Production Settings
```bash
cp cms_core/local_settings_production.py cms_core/local_settings.py
```

### 4.2 Run Database Migrations
```bash
source venv/bin/activate
python manage.py migrate
```

### 4.3 Create Superuser
```bash
python manage.py createsuperuser
```

### 4.4 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4.5 Test the Application
```bash
python manage.py runserver 0.0.0.0:8000
```
Visit `http://your-vps-ip:8000` to test. Stop the server with `Ctrl+C`.

## Step 5: Gunicorn Configuration

The `gunicorn.conf.py` file is already configured with optimal settings for production. Key configurations:

- **Bind**: `127.0.0.1:8000` (matches your nginx config)
- **Workers**: CPU cores × 2 + 1
- **Logging**: Configured for `/var/log/arc/`
- **Security**: Proper user/group settings

## Step 6: Systemd Service Setup

### 6.1 Create Log Directory
```bash
sudo mkdir -p /var/log/arc
sudo chown ubuntu:ubuntu /var/log/arc
```

### 6.2 Install Systemd Service
```bash
sudo cp arc-cms.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable arc-cms
```

### 6.3 Start the Service
```bash
sudo systemctl start arc-cms
sudo systemctl status arc-cms
```

## Step 7: Nginx Configuration

Your existing nginx configuration should already handle the backend. Verify these paths in your nginx config:

```nginx
# Static files for Django
location /static/ {
    alias /home/ubuntu/projects/arc-deploy/arc_cms/staticfiles/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Media files for Django
location /media/ {
    alias /home/ubuntu/projects/arc-deploy/arc_cms/media/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Django backend
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $server_name;
    proxy_redirect off;
}
```

### 7.1 Test Nginx Configuration
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Step 8: Security and Permissions

### 8.1 Set Proper File Permissions
```bash
cd /home/ubuntu/projects/arc-deploy/arc_cms
chmod 755 .
chmod 644 *.py
chmod 600 cms_core/local_settings.py
chmod +x deploy.sh
```

### 8.2 Create Media and Static Directories
```bash
mkdir -p media staticfiles
chmod 755 media staticfiles
```

## Step 9: Automated Deployment

### 9.1 Run the Deployment Script
```bash
cd /home/ubuntu/projects/arc-deploy/arc_cms
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Create necessary directories
- Setup virtual environment
- Install dependencies
- Configure database
- Run Django commands
- Setup systemd service
- Start services
- Verify deployment

## Step 10: Verification and Testing

### 10.1 Check Service Status
```bash
sudo systemctl status arc-cms
sudo journalctl -u arc-cms -f
```

### 10.2 Test API Endpoints
```bash
# Test main API
curl -I https://api.arc.pingtech.dev/

# Test admin interface
curl -I https://api.arc.pingtech.dev/admin/

# Test static files
curl -I https://api.arc.pingtech.dev/static/admin/css/base.css
```

### 10.3 Check Logs
```bash
# Application logs
tail -f /var/log/arc/gunicorn_error.log
tail -f /var/log/arc/gunicorn_access.log

# System logs
sudo journalctl -u arc-cms -f
```

## Step 11: Production Optimizations

### 11.1 Enable Gzip Compression
Your nginx config already includes gzip compression.

### 11.2 Setup Log Rotation
Create `/etc/logrotate.d/arc-cms`:
```
/var/log/arc/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
    postrotate
        systemctl reload arc-cms
    endscript
}
```

### 11.3 Monitor Resources
```bash
# Check memory usage
free -h

# Check disk usage
df -h

# Check running processes
ps aux | grep gunicorn
```

## Step 12: Maintenance Commands

### 12.1 Service Management
```bash
# Start/Stop/Restart service
sudo systemctl start arc-cms
sudo systemctl stop arc-cms
sudo systemctl restart arc-cms
sudo systemctl reload arc-cms

# Check status
sudo systemctl status arc-cms
```

### 12.2 Django Management
```bash
cd /home/ubuntu/projects/arc-deploy/arc_cms
source venv/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### 12.3 Log Monitoring
```bash
# Real-time logs
sudo journalctl -u arc-cms -f

# Application logs
tail -f /var/log/arc/gunicorn_error.log
tail -f /var/log/arc/gunicorn_access.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Step 13: Troubleshooting

### 13.1 Common Issues

**Service won't start:**
```bash
sudo systemctl status arc-cms
sudo journalctl -u arc-cms --no-pager
```

**Database connection issues:**
- Check MySQL service: `sudo systemctl status mysql`
- Verify database credentials in `local_settings.py`
- Test connection: `mysql -u arc_user -p arc_cms`

**Static files not loading:**
- Check nginx config: `sudo nginx -t`
- Verify static files path in nginx config
- Run: `python manage.py collectstatic --noinput`

**Permission issues:**
```bash
sudo chown -R ubuntu:ubuntu /home/ubuntu/projects/arc-deploy/arc_cms
sudo chmod -R 755 /home/ubuntu/projects/arc-deploy/arc_cms
```

### 13.2 Performance Monitoring
```bash
# Check system resources
htop
iostat -x 1

# Check network connections
netstat -tlnp | grep :8000
ss -tlnp | grep :8000
```

## Step 14: Backup Strategy

### 14.1 Database Backup
```bash
# Create backup script
cat > /home/ubuntu/backup_db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u arc_user -p arc_cms > /home/ubuntu/backups/arc_cms_$DATE.sql
gzip /home/ubuntu/backups/arc_cms_$DATE.sql
EOF

chmod +x /home/ubuntu/backup_db.sh
```

### 14.2 Media Files Backup
```bash
# Create media backup script
cat > /home/ubuntu/backup_media.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /home/ubuntu/backups/media_$DATE.tar.gz /home/ubuntu/projects/arc-deploy/arc_cms/media/
EOF

chmod +x /home/ubuntu/backup_media.sh
```

## Step 15: SSL and Security

### 15.1 SSL Certificate
Your existing Let's Encrypt certificates should work for the subdomain.

### 15.2 Security Headers
Your nginx config already includes security headers.

### 15.3 Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## Final Verification

After completing all steps, verify your deployment:

1. **Service Status**: `sudo systemctl status arc-cms`
2. **API Access**: Visit `https://api.arc.pingtech.dev/`
3. **Admin Access**: Visit `https://api.arc.pingtech.dev/admin/`
4. **Static Files**: Check if CSS/JS files load correctly
5. **Database**: Verify data persistence

## Support and Maintenance

- **Logs**: Always check logs first when troubleshooting
- **Updates**: Use the deployment script for updates
- **Monitoring**: Set up monitoring for production use
- **Backups**: Implement regular backup procedures

Your ARC CMS should now be successfully deployed and accessible at `https://api.arc.pingtech.dev`!
