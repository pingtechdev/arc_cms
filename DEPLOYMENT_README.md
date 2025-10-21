# ARC CMS uWSGI Deployment Guide

## Overview
This guide explains how to deploy the ARC CMS application using uWSGI with dynamic path configuration, making it location-independent.

## Changes Made

### 1. Removed Gunicorn Configuration
- ✅ Deleted `gunicorn.conf.py`
- ✅ Updated systemd service to use uWSGI instead of Gunicorn

### 2. Dynamic Path Configuration
- ✅ Updated `uwsgi.ini` to use relative paths
- ✅ Updated `local_settings.py` to use dynamic project root detection
- ✅ Updated systemd service to use environment variables
- ✅ Updated Nginx configuration to use environment variables

### 3. Created Deployment Script
- ✅ Created `deploy.sh` script for automated deployment
- ✅ Script automatically detects project location
- ✅ Generates systemd and Nginx configurations with correct paths

## Files Modified

1. **`uwsgi.ini`** - Now uses relative paths and dynamic configuration
2. **`arc-cms.service`** - Updated to use environment variables
3. **`cms_core/local_settings.py`** - Uses dynamic project root detection
4. **`nginx_arc_cms.conf`** - Uses environment variables for paths
5. **`deploy.sh`** - New deployment script (executable)

## Deployment Instructions

### Step 1: Run the Deployment Script
```bash
cd /path/to/your/arc_cms
./deploy.sh
```

### Step 2: Complete System Setup
The script will provide you with the exact commands to run. Typically:

```bash
# Copy systemd service file
sudo cp /tmp/arc-cms.service /etc/systemd/system/

# Copy nginx configuration
sudo cp /tmp/nginx_arc_cms.conf /etc/nginx/sites-available/arc_cms
sudo ln -sf /etc/nginx/sites-available/arc_cms /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Reload systemd and start services
sudo systemctl daemon-reload
sudo systemctl enable arc-cms
sudo systemctl start arc-cms
sudo systemctl restart nginx
```

### Step 3: Verify Deployment
```bash
# Check service status
sudo systemctl status arc-cms
sudo systemctl status nginx

# Check logs
sudo journalctl -u arc-cms -f
tail -f /path/to/your/arc_cms/logs/uwsgi.log
```

## Key Benefits

### 1. Location Independence
- ✅ Project can be moved to any directory without breaking
- ✅ All paths are automatically detected and configured
- ✅ No hardcoded paths in configuration files

### 2. Easy Deployment
- ✅ Single script handles all configuration
- ✅ Automatic path detection and setup
- ✅ Consistent deployment across different environments

### 3. Maintainability
- ✅ Configuration files are template-based
- ✅ Easy to update and modify
- ✅ Clear separation of concerns

## Configuration Details

### uWSGI Configuration (`uwsgi.ini`)
- Uses relative paths with `%(chdir)` variables
- Socket: `%(chdir)/tmp/arc_cms.sock`
- PID file: `%(chdir)/tmp/arc_cms_uwsgi.pid`
- Log file: `%(chdir)/logs/uwsgi.log`

### Systemd Service (`arc-cms.service`)
- Uses environment variables for paths
- Automatically sets `ARC_CMS_DIR` environment variable
- Dynamic `WorkingDirectory` and `PYTHONPATH`

### Django Settings (`local_settings.py`)
- Dynamic project root detection using `os.path.dirname()`
- All file paths relative to project root
- No hardcoded absolute paths

### Nginx Configuration
- Uses environment variables for static/media paths
- Socket path dynamically configured
- Template-based configuration generation

## Troubleshooting

### Common Issues

1. **Permission Errors**
   ```bash
   sudo chown -R ubuntu:ubuntu /path/to/your/arc_cms
   sudo chmod -R 755 /path/to/your/arc_cms
   ```

2. **Socket Permission Issues**
   ```bash
   sudo chmod 666 /path/to/your/arc_cms/tmp/arc_cms.sock
   ```

3. **Service Not Starting**
   ```bash
   sudo journalctl -u arc-cms -f
   # Check for specific error messages
   ```

4. **Nginx Configuration Issues**
   ```bash
   sudo nginx -t
   # Fix any configuration errors
   sudo systemctl reload nginx
   ```

### Log Locations
- uWSGI logs: `/path/to/your/arc_cms/logs/uwsgi.log`
- System logs: `sudo journalctl -u arc-cms`
- Nginx logs: `/var/log/nginx/arc_cms_*.log`

## Moving the Project

To move the project to a new location:

1. **Copy the project** to the new location
2. **Run the deployment script** from the new location:
   ```bash
   cd /new/path/to/arc_cms
   ./deploy.sh
   ```
3. **Follow the deployment instructions** provided by the script
4. **Update any external references** (if any) to the new path

The project is now completely location-independent!
