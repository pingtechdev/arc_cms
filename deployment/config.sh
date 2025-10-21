#!/bin/bash

# ARC CMS Backend Deployment Configuration
# This file contains all configurable paths and settings for the backend

# Base paths
export HOME_DIR="/home"
export PROJECTS_DIR="$HOME_DIR"
export BACKEND_DIR="$PROJECTS_DIR/arc_cms"

# User configuration
export DEPLOY_USER="ubuntu"
export DEPLOY_GROUP="ubuntu"

# Domain configuration
export FRONTEND_DOMAIN="arc.pingtech.dev"
export BACKEND_DOMAIN="api.arc.pingtech.dev"

# Service configuration
export BACKEND_SERVICE_NAME="arc-cms"
export BACKEND_PORT="8001"

# Nginx configuration
export NGINX_SITES_AVAILABLE="/etc/nginx/sites-available"
export NGINX_SITES_ENABLED="/etc/nginx/sites-enabled"
export NGINX_LOG_DIR="/var/log/nginx"

# SSL configuration
export SSL_CERT_DIR="/etc/letsencrypt/live"
export SSL_CERT_BACKEND="$SSL_CERT_DIR/$BACKEND_DOMAIN/fullchain.pem"
export SSL_KEY_BACKEND="$SSL_CERT_DIR/$BACKEND_DOMAIN/privkey.pem"

# Database configuration
export DB_NAME="arc_cms"
export DB_USER="arc_user"
export DB_PASSWORD="arc_secure_password_2024"
export DB_HOST="localhost"
export DB_PORT="3306"

# Log directories
export LOG_DIR="/var/log/arc"
export BACKEND_LOG_DIR="$LOG_DIR"

# Socket and PID files
export BACKEND_SOCKET="$BACKEND_DIR/tmp/arc_cms.sock"
export BACKEND_PID="$BACKEND_DIR/tmp/arc_cms_uwsgi.pid"
export BACKEND_STATS="$BACKEND_DIR/tmp/arc_cms_stats.sock"

# Static and media directories
export BACKEND_STATIC_ROOT="$BACKEND_DIR/staticfiles"
export BACKEND_MEDIA_ROOT="$BACKEND_DIR/media"

# Systemd service file
export SYSTEMD_SERVICE_FILE="/etc/systemd/system/$BACKEND_SERVICE_NAME.service"

# Colors for output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export PURPLE='\033[0;35m'
export NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}[HEADER]${NC} $1"
}

# Function to check if directory exists and create if needed
ensure_directory() {
    local dir="$1"
    local owner="$2"
    local group="$3"
    local permissions="$4"
    
    if [ ! -d "$dir" ]; then
        print_status "Creating directory: $dir"
        sudo mkdir -p "$dir"
    fi
    
    if [ -n "$owner" ] && [ -n "$group" ]; then
        sudo chown "$owner:$group" "$dir"
    fi
    
    if [ -n "$permissions" ]; then
        sudo chmod "$permissions" "$dir"
    fi
}

# Function to check if file exists
check_file_exists() {
    local file="$1"
    if [ -f "$file" ]; then
        return 0
    else
        return 1
    fi
}

# Function to check if directory exists
check_dir_exists() {
    local dir="$1"
    if [ -d "$dir" ]; then
        return 0
    else
        return 1
    fi
}

# Function to get absolute path
get_absolute_path() {
    local path="$1"
    if [ -d "$path" ]; then
        cd "$path" && pwd
    else
        echo "$path"
    fi
}

# Function to validate configuration
validate_config() {
    print_status "Validating configuration..."
    
    # Check if user exists
    if ! id "$DEPLOY_USER" &>/dev/null; then
        print_error "User '$DEPLOY_USER' does not exist."
        return 1
    fi
    
    # Check if group exists
    if ! getent group "$DEPLOY_GROUP" &>/dev/null; then
        print_error "Group '$DEPLOY_GROUP' does not exist."
        return 1
    fi
    
    # Check if backend directory exists
    if [ ! -d "$BACKEND_DIR" ]; then
        print_warning "Backend directory does not exist: $BACKEND_DIR"
        print_status "Please ensure you're running this from the correct location."
        return 1
    fi
    
    print_success "Configuration validation passed."
    return 0
}

# Function to show configuration
show_config() {
    print_header "Backend Deployment Configuration"
    echo "=========================================="
    echo "Base Paths:"
    echo "  Home Directory: $HOME_DIR"
    echo "  Projects Directory: $PROJECTS_DIR"
    echo "  Backend Directory: $BACKEND_DIR"
    echo ""
    echo "Domains:"
    echo "  Frontend: $FRONTEND_DOMAIN"
    echo "  Backend: $BACKEND_DOMAIN"
    echo ""
    echo "Service Configuration:"
    echo "  Service Name: $BACKEND_SERVICE_NAME"
    echo "  Backend Port: $BACKEND_PORT"
    echo "  User: $DEPLOY_USER"
    echo "  Group: $DEPLOY_GROUP"
    echo ""
    echo "Database:"
    echo "  Name: $DB_NAME"
    echo "  User: $DB_USER"
    echo "  Host: $DB_HOST:$DB_PORT"
    echo "=========================================="
}
