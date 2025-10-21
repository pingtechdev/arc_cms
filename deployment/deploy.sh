#!/bin/bash

# ARC CMS Backend Deployment Script
# This script deploys the Django/Wagtail CMS backend

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Change to the deployment directory to ensure we're in the right place
cd "$SCRIPT_DIR"

# Validate configuration
if ! validate_config; then
    print_error "Configuration validation failed."
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if required commands exist
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    if ! command_exists pip3; then
        print_error "pip3 is not installed. Please install pip3 first."
        exit 1
    fi
    
    if ! command_exists uwsgi; then
        print_error "uWSGI is not installed. Please install uWSGI first."
        exit 1
    fi
    
    if ! command_exists nginx; then
        print_error "nginx is not installed. Please install nginx first."
        exit 1
    fi
    
    print_success "All requirements are met."
}

# Function to create project directory structure
create_directories() {
    print_status "Creating project directories..."
    
    # Create backend directories
    ensure_directory "$BACKEND_DIR/logs" "$DEPLOY_USER" "$DEPLOY_GROUP" "755"
    ensure_directory "$BACKEND_DIR/tmp" "$DEPLOY_USER" "$DEPLOY_GROUP" "755"
    ensure_directory "$BACKEND_DIR/staticfiles" "$DEPLOY_USER" "$DEPLOY_GROUP" "755"
    ensure_directory "$BACKEND_DIR/media" "$DEPLOY_USER" "$DEPLOY_GROUP" "755"
    ensure_directory "$LOG_DIR" "$DEPLOY_USER" "$DEPLOY_GROUP" "755"
    
    print_success "Directories created successfully."
}

# Function to setup Python virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    cd "$BACKEND_DIR"
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        print_warning "requirements.txt not found. Installing basic Django packages..."
        pip install django wagtail mysqlclient djangorestframework django-cors-headers
    fi
    
    print_success "Virtual environment setup complete."
}

# Function to configure Django
configure_django() {
    print_status "Configuring Django..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # Create local settings if it doesn't exist
    if [ ! -f "cms_core/local_settings.py" ]; then
        print_warning "Creating local_settings.py from template..."
        cat > cms_core/local_settings.py << EOF
# Local settings for production
import os

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '$DB_NAME',
        'USER': '$DB_USER',
        'PASSWORD': '$DB_PASSWORD',
        'HOST': '$DB_HOST',
        'PORT': '$DB_PORT',
    }
}

# Security settings
SECRET_KEY = 'your-secret-key-here'
DEBUG = False
ALLOWED_HOSTS = ['$BACKEND_DOMAIN', 'localhost', '127.0.0.1']

# Static files
STATIC_ROOT = '$BACKEND_STATIC_ROOT'
MEDIA_ROOT = '$BACKEND_MEDIA_ROOT'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '$LOG_DIR/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
EOF
        print_warning "Please edit cms_core/local_settings.py with your actual database credentials and secret key."
    fi
    
    # Run migrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    print_success "Django configuration complete."
}

# Function to setup systemd service
setup_systemd() {
    print_status "Setting up systemd service..."
    
    # Check if envsubst is available
    if command -v envsubst >/dev/null 2>&1; then
        # Create systemd service file with variables substituted
        envsubst < systemd/arc-cms.service > /tmp/arc-cms.service
    else
        print_warning "envsubst not found, using sed for variable substitution..."
        # Use sed to substitute variables
        sed -e "s|\${DEPLOY_USER}|$DEPLOY_USER|g" \
            -e "s|\${DEPLOY_GROUP}|$DEPLOY_GROUP|g" \
            -e "s|\${BACKEND_DIR}|$BACKEND_DIR|g" \
            -e "s|\${LOG_DIR}|$LOG_DIR|g" \
            -e "s|\${BACKEND_SERVICE_NAME}|$BACKEND_SERVICE_NAME|g" \
            systemd/arc-cms.service > /tmp/arc-cms.service
    fi
    
    # Copy service file
    sudo cp /tmp/arc-cms.service "$SYSTEMD_SERVICE_FILE"
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable "$BACKEND_SERVICE_NAME"
    
    print_success "Systemd service configured."
}

# Function to setup nginx
setup_nginx() {
    print_status "Setting up nginx configuration..."
    
    # Check if envsubst is available
    if command -v envsubst >/dev/null 2>&1; then
        # Create nginx configuration with variables substituted
        envsubst < nginx/arc_cms.conf > /tmp/arc_cms.conf
    else
        print_warning "envsubst not found, using sed for variable substitution..."
        # Use sed to substitute variables
        sed -e "s|\${BACKEND_DOMAIN}|$BACKEND_DOMAIN|g" \
            -e "s|\${BACKEND_PORT}|$BACKEND_PORT|g" \
            -e "s|\${FRONTEND_DOMAIN}|$FRONTEND_DOMAIN|g" \
            -e "s|\${BACKEND_STATIC_ROOT}|$BACKEND_STATIC_ROOT|g" \
            -e "s|\${BACKEND_MEDIA_ROOT}|$BACKEND_MEDIA_ROOT|g" \
            -e "s|\${BACKEND_SOCKET}|$BACKEND_SOCKET|g" \
            -e "s|\${SSL_CERT_BACKEND}|$SSL_CERT_BACKEND|g" \
            -e "s|\${SSL_KEY_BACKEND}|$SSL_KEY_BACKEND|g" \
            -e "s|\${NGINX_LOG_DIR}|$NGINX_LOG_DIR|g" \
            nginx/arc_cms.conf > /tmp/arc_cms.conf
    fi
    
    # Copy nginx configuration
    sudo cp /tmp/arc_cms.conf "$NGINX_SITES_AVAILABLE/arc_cms.conf"
    
    # Enable site
    sudo ln -sf "$NGINX_SITES_AVAILABLE/arc_cms.conf" "$NGINX_SITES_ENABLED/"
    
    # Remove default site if it exists
    sudo rm -f "$NGINX_SITES_ENABLED/default"
    
    # Test nginx configuration
    if sudo nginx -t; then
        print_success "Nginx configuration is valid."
    else
        print_error "Nginx configuration test failed."
        exit 1
    fi
    
    print_success "Nginx configuration complete."
}

# Function to start services
start_services() {
    print_status "Starting services..."
    
    # Start the application service
    sudo systemctl start "$BACKEND_SERVICE_NAME"
    
    # Restart nginx
    sudo systemctl restart nginx
    
    # Check service status
    if systemctl is-active --quiet "$BACKEND_SERVICE_NAME"; then
        print_success "Backend service is running."
    else
        print_error "Failed to start backend service."
        sudo systemctl status "$BACKEND_SERVICE_NAME"
        exit 1
    fi
    
    if systemctl is-active --quiet nginx; then
        print_success "Nginx is running."
    else
        print_error "Failed to start nginx."
        sudo systemctl status nginx
        exit 1
    fi
    
    print_success "All services started successfully."
}

# Function to verify deployment
verify_deployment() {
    print_status "Verifying deployment..."
    
    # Check if service is running
    if ! systemctl is-active --quiet "$BACKEND_SERVICE_NAME"; then
        print_error "Backend service is not running."
        return 1
    fi
    
    # Check if nginx is running
    if ! systemctl is-active --quiet nginx; then
        print_error "Nginx is not running."
        return 1
    fi
    
    # Check if socket file exists (if using Unix socket)
    if [ -S "$BACKEND_SOCKET" ]; then
        print_success "Unix socket file exists."
    else
        print_warning "Unix socket file not found. Using TCP port $BACKEND_PORT."
    fi
    
    # Test HTTP response
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$BACKEND_PORT/health/" | grep -q "200"; then
        print_success "Backend is responding to health checks."
    else
        print_warning "Backend health check failed. Check logs for details."
    fi
    
    print_success "Deployment verification complete."
}

# Main deployment function
main() {
    echo "=========================================="
    echo "🚀 ARC CMS Backend Deployment Script"
    echo "=========================================="
    echo "Project Directory: $BACKEND_DIR"
    echo "Service Name: $BACKEND_SERVICE_NAME"
    echo "Started at: $(date)"
    echo "=========================================="
    
    # Check if project directory exists
    if [ ! -d "$BACKEND_DIR" ]; then
        print_error "Project directory does not exist: $BACKEND_DIR"
        print_status "Please ensure you're running this from the correct location."
        exit 1
    fi
    
    # Run deployment steps
    check_requirements
    create_directories
    setup_venv
    configure_django
    setup_systemd
    setup_nginx
    start_services
    verify_deployment
    
    echo "=========================================="
    print_success "🎉 Backend deployment completed successfully!"
    echo "Backend will be available at: https://$BACKEND_DOMAIN"
    echo "Admin panel: https://$BACKEND_DOMAIN/admin/"
    echo "Deployment finished at: $(date)"
    echo "=========================================="
}

# Run main function
main "$@"