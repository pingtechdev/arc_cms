# Gunicorn configuration file for ARC CMS
import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/arc/gunicorn_access.log"
errorlog = "/var/log/arc/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "arc_cms_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/run/arc_cms_gunicorn.pid"
user = "ubuntu"
group = "ubuntu"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Preload app for better performance
preload_app = True

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=cms_core.settings',
    'PYTHONPATH=/home/ubuntu/projects/arc-deploy/arc_cms',
]

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Graceful timeout for worker restart
graceful_timeout = 30

# Enable worker recycling
preload_app = True
