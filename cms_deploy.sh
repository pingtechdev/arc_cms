#!/bin/bash

echo "🚀 Deploying Django CMS..."

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --settings=cms_core.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=cms_core.settings_production

# Restart Django service
sudo systemctl restart arc-django

echo "✅ Django CMS deployed successfully!"
