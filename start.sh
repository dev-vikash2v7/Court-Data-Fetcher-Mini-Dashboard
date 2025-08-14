#!/bin/bash

# Production startup script for Render deployment

echo "Starting Court Scraper Application..."

# Initialize database
python -c "from app import init_db; init_db()"

# Start the application with gunicorn
exec gunicorn --config gunicorn.conf.py app:app
