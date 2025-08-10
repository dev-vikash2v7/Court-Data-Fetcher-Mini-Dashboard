#!/bin/bash

echo "========================================"
echo "Court Data Fetcher - Installation Script"
echo "========================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "macOS: brew install python3"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

echo "Python found. Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the app: python app.py"
echo "3. Open browser: http://localhost:5000"
echo
echo "Note: Make sure you have Chrome browser installed for web scraping functionality."
echo "Ubuntu/Debian: sudo apt-get install chromium-browser"
echo "macOS: brew install --cask google-chrome"
echo "CentOS/RHEL: sudo yum install chromium"
echo

