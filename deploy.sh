#!/bin/bash

# ARC CMS Deployment Script
# This script deploys the Django CMS application to production

set -e  # Exit on any error

# Configuration
PROJECT_DIR="/home/ubuntu/projects/arc-deploy/arc_cms"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="arc-cms"
LOG_DIR="/var/log/arc"

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to create directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create log directory
    sudo mkdir -p "$LOG_DIR"
    sudo chown ubuntu:ubuntu "$LOG_DIR"
    
    # Create staticfiles directory
    mkdir -p "$PROJECT_DIR/staticfiles"
    
    # Create media directory
    mkdir -p "$PROJECT_DIR/media"
}

# Function to setup virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment and install dependencies
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install gunicorn  # Ensure gunicorn is installed
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    # Check if MySQL is running
    if ! systemctl is-active --quiet mysql; then
        print_warning "MySQL is not running. Starting MySQL service..."
        sudo systemctl start mysql
    fi
    
    # Create database and user (you'll need to update these credentials)
    print_warning "Please update the database credentials in cms_core/local_settings_production.py"
    print_warning "You may need to run these MySQL commands manually:"
    echo "CREATE DATABASE IF NOT EXISTS arc_cms;"
    echo "CREATE USER IF NOT EXISTS 'arc_user'@'localhost' IDENTIFIED BY 'your_secure_password';"
    echo "GRANT ALL PRIVILEGES ON arc_cms.* TO 'arc_user'@'localhost';"
    echo "FLUSH PRIVILEGES;"
}

# Function to run Django commands
run_django_commands() {
    print_status "Running Django management commands..."
    
    cd "$PROJECT_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Copy production settings
    # cp cms_core/local_settings_production.py cms_core/local_settings.py
    
    # Run migrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    # Create superuser (optional - you can skip this if you already have one)
    print_warning "You may want to create a superuser manually:"
    echo "python manage.py createsuperuser"
}

# Function to setup systemd service
setup_systemd_service() {
    print_status "Setting up systemd service..."
    
    # Copy service file
    sudo cp arc-cms.service /etc/systemd/system/
    
    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    
    print_status "Service installed and enabled"
}

# Function to start services
start_services() {
    print_status "Starting services..."
    
    # Start the Django application
    sudo systemctl start "$SERVICE_NAME"
    
    # Check if service is running
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        print_status "ARC CMS service is running successfully"
    else
        print_error "Failed to start ARC CMS service"
        sudo systemctl status "$SERVICE_NAME"
        exit 1
    fi
}

# Function to setup nginx (if needed)
setup_nginx() {
    print_status "Nginx configuration should already be set up based on your existing config"
    print_status "Make sure your nginx config points to the correct paths:"
    echo "- Static files: $PROJECT_DIR/staticfiles/"
    echo "- Media files: $PROJECT_DIR/media/"
    echo "- Backend proxy: http://127.0.0.1:8000"
    
    # Test nginx configuration
    if command_exists nginx; then
        sudo nginx -t
        if [ $? -eq 0 ]; then
            print_status "Nginx configuration is valid"
            sudo systemctl reload nginx
        else
            print_error "Nginx configuration has errors"
        fi
    fi
}

# Function to check deployment
check_deployment() {
    print_status "Checking deployment status..."
    
    # Check if service is running
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        print_status "✓ ARC CMS service is running"
    else
        print_error "✗ ARC CMS service is not running"
        return 1
    fi
    
    # Check if port 8000 is listening
    if netstat -tlnp | grep -q ":8000"; then
        print_status "✓ Port 8000 is listening"
    else
        print_error "✗ Port 8000 is not listening"
        return 1
    fi
    
    # Check nginx status
    if systemctl is-active --quiet nginx; then
        print_status "✓ Nginx is running"
    else
        print_warning "⚠ Nginx is not running"
    fi
    
    print_status "Deployment check completed"
}

# Function to show useful commands
show_commands() {
    print_status "Useful commands for managing your deployment:"
    echo ""
    echo "Service management:"
    echo "  sudo systemctl status $SERVICE_NAME"
    echo "  sudo systemctl start $SERVICE_NAME"
    echo "  sudo systemctl stop $SERVICE_NAME"
    echo "  sudo systemctl restart $SERVICE_NAME"
    echo "  sudo systemctl reload $SERVICE_NAME"
    echo ""
    echo "View logs:"
    echo "  sudo journalctl -u $SERVICE_NAME -f"
    echo "  tail -f $LOG_DIR/gunicorn_error.log"
    echo "  tail -f $LOG_DIR/gunicorn_access.log"
    echo ""
    echo "Django management:"
    echo "  cd $PROJECT_DIR"
    echo "  source $VENV_DIR/bin/activate"
    echo "  python manage.py <command>"
    echo ""
    echo "Test the API:"
    echo "  curl -I https://api.arc.pingtech.dev/"
    echo "  curl -I https://api.arc.pingtech.dev/admin/"
}

# Main deployment function
main() {
    print_status "Starting ARC CMS deployment..."
    
    # Check if running as ubuntu user
    if [ "$USER" != "ubuntu" ] && ["$USER" != "root"]; then
        print_error "This script should be run as the ubuntu user"
        exit 1
    fi
    
    # Check if we're in the right directory
    if [ ! -f "manage.py" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Run deployment steps
    create_directories
    setup_venv
    setup_database
    run_django_commands
    setup_systemd_service
    start_services
    setup_nginx
    check_deployment
    show_commands
    
    print_status "Deployment completed successfully!"
    print_status "Your Django CMS should now be accessible at https://api.arc.pingtech.dev"
}

# Run main function
main "$@"
