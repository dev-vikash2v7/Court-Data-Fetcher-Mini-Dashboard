#!/usr/bin/env python3
"""
Test script to verify Chrome setup works in production environment
"""

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_chrome_setup():
    """Test if Chrome can be set up properly"""
    try:
        print("Testing Chrome setup...")
        
        # Set up Chrome options for production
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        print("Chrome options configured...")
        
        # Set up service with webdriver-manager
        service = Service(ChromeDriverManager().install())
        print("ChromeDriver service created...")
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome driver created successfully!")
        
        # Test navigation
        driver.get("https://www.google.com")
        print(f"Page title: {driver.title}")
        
        # Clean up
        driver.quit()
        print("Chrome test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Chrome test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_chrome_setup()
    sys.exit(0 if success else 1)
