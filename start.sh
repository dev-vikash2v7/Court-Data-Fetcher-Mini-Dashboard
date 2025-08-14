#!/bin/bash

# Production startup script for Render deployment

echo "Starting Court Scraper Application..."

# Test Chrome setup first
echo "Testing Chrome setup..."
python test_chrome.py
if [ $? -ne 0 ]; then
    echo "Chrome setup test failed!"
    exit 1
fi

# Initialize database
echo "Initializing database..."
python -c "from app import init_db; init_db()"

# Start the application with gunicorn
echo "Starting application with gunicorn..."
exec gunicorn --config gunicorn.conf.py app:app
