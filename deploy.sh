#!/bin/bash

# ARC CMS Deployment Script
# This script sets up the ARC CMS application with dynamic paths

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the current directory (where the script is located)
ARC_CMS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
print_status "ARC CMS Directory: $ARC_CMS_DIR"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p "$ARC_CMS_DIR/logs"
mkdir -p "$ARC_CMS_DIR/tmp"
mkdir -p "$ARC_CMS_DIR/staticfiles"
mkdir -p "$ARC_CMS_DIR/media"

# Set permissions
print_status "Setting permissions..."
chmod 755 "$ARC_CMS_DIR/logs"
chmod 755 "$ARC_CMS_DIR/tmp"
chmod 755 "$ARC_CMS_DIR/staticfiles"
chmod 755 "$ARC_CMS_DIR/media"

# Update uwsgi.ini with current directory
print_status "Updating uWSGI configuration..."
sed -i "s|%(chdir)|$ARC_CMS_DIR|g" "$ARC_CMS_DIR/uwsgi.ini"

# Create systemd service file with current directory
print_status "Creating systemd service file..."
cat > /tmp/arc-cms.service << EOF
[Unit]
Description=ARC CMS Django Application with uWSGI
After=network.target mysql.service
Wants=mysql.service

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=$ARC_CMS_DIR
Environment=DJANGO_SETTINGS_MODULE=cms_core.settings
Environment=PYTHONPATH=$ARC_CMS_DIR
Environment=ARC_CMS_DIR=$ARC_CMS_DIR
ExecStart=$ARC_CMS_DIR/venv/bin/uwsgi --ini uwsgi.ini
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s QUIT \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$ARC_CMS_DIR
ReadWritePaths=/var/log/arc
ReadWritePaths=/var/run
ReadWritePaths=/tmp

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration with current directory
print_status "Creating Nginx configuration..."
cat > /tmp/nginx_arc_cms.conf << EOF
# Nginx configuration for ARC CMS with uWSGI
server {
    listen 80;
    server_name api.arc.pingtech.dev arc.pingtech.dev;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.arc.pingtech.dev arc.pingtech.dev;
    
    # SSL Configuration (update paths as needed)
    ssl_certificate /etc/ssl/certs/arc.pingtech.dev.crt;
    ssl_certificate_key /etc/ssl/private/arc.pingtech.dev.key;
    
    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Client max body size for file uploads
    client_max_body_size 100M;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Static files
    location /static/ {
        alias $ARC_CMS_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Media files
    location /media/ {
        alias $ARC_CMS_DIR/media/;
        expires 1y;
        add_header Cache-Control "public";
        access_log off;
    }
    
    # Wagtail admin static files
    location /admin/static/ {
        alias $ARC_CMS_DIR/staticfiles/admin/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Wagtail admin media
    location /admin/media/ {
        alias $ARC_CMS_DIR/media/;
        expires 1y;
        add_header Cache-Control "public";
        access_log off;
    }
    
    # Main application
    location / {
        include uwsgi_params;
        uwsgi_pass unix:$ARC_CMS_DIR/tmp/arc_cms.sock;
        uwsgi_param Host \$host;
        uwsgi_param X-Real-IP \$remote_addr;
        uwsgi_param X-Forwarded-For \$proxy_add_x_forwarded_for;
        uwsgi_param X-Forwarded-Proto \$scheme;
        uwsgi_param X-Forwarded-Host \$host;
        uwsgi_param X-Forwarded-Port \$server_port;
        
        # Timeouts
        uwsgi_connect_timeout 60s;
        uwsgi_send_timeout 60s;
        uwsgi_read_timeout 60s;
        
        # Buffer settings
        uwsgi_buffer_size 4k;
        uwsgi_buffers 8 4k;
        uwsgi_busy_buffers_size 8k;
    }
    
    # Health check endpoint
    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Logging
    access_log /var/log/nginx/arc_cms_access.log;
    error_log /var/log/nginx/arc_cms_error.log;
}
EOF

print_status "Deployment configuration created successfully!"
print_status "To complete the deployment, run the following commands:"
echo ""
echo "1. Copy systemd service file:"
echo "   sudo cp /tmp/arc-cms.service /etc/systemd/system/"
echo ""
echo "2. Copy nginx configuration:"
echo "   sudo cp /tmp/nginx_arc_cms.conf /etc/nginx/sites-available/arc_cms"
echo "   sudo ln -sf /etc/nginx/sites-available/arc_cms /etc/nginx/sites-enabled/"
echo ""
echo "3. Test nginx configuration:"
echo "   sudo nginx -t"
echo ""
echo "4. Reload systemd and start services:"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable arc-cms"
echo "   sudo systemctl start arc-cms"
echo "   sudo systemctl restart nginx"
echo ""
echo "5. Check service status:"
echo "   sudo systemctl status arc-cms"
echo "   sudo systemctl status nginx"
