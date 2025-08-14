
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import logging
import os
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DelhiHighCourtScraper:
    """
    Scraper class for Delhi High Court website - Production Ready
    """
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with production-ready anti-detection measures"""
        try:
            chrome_options = Options()
            
            # Always run headless in production
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-features=TranslateUI')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Production-specific options for Render/Heroku
            chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            
            # Use webdriver-manager to automatically download and manage Chrome driver
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 15)  # Increased timeout for production
            
            logger.info("Chrome WebDriver setup successful (headless mode)")
        except Exception as e:
            logger.error(f"Failed to setup Chrome WebDriver: {e}")
            raise
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay to avoid detection (reduced for production)"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def navigate_to_court_website(self):
        """Navigate to Delhi High Court website"""
        try:
            logger.info("Navigating to Delhi High Court website...")
            # Navigate directly to the case status page
            self.driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")
            self.random_delay(2, 4)
            
            # Wait for page to load and form to be present
            self.wait.until(EC.presence_of_element_located((By.ID, "case_type")))
            logger.info("Successfully loaded Delhi High Court case status page")
            
        except Exception as e:
            logger.error(f"Failed to navigate to court website: {e}")
            raise
    
    def get_captcha_code(self):
        """Get the captcha code from the page"""
        try:
            # Wait for captcha to load
            captcha_element = self.wait.until(EC.presence_of_element_located((By.ID, "captcha-code")))
            captcha_code = captcha_element.text.strip()

            logger.info(f"Captcha code found: {captcha_code}")
            return captcha_code
        except Exception as e:
            logger.error(f"Error getting captcha code: {e}")
            return None
    
    def fill_case_search_form(self, case_type, case_number, filing_year):
        """Fill the case search form with provided details"""
        try:
            logger.info(f"Filling search form: {case_type}/{case_number}/{filing_year}")
            
            # Fill case type dropdown
            case_type_select = self.driver.find_element(By.ID, "case_type")
            from selenium.webdriver.support.ui import Select
            select_case_type = Select(case_type_select)
            select_case_type.select_by_value(case_type)
            logger.info(f"Selected case type: {case_type}")
            self.random_delay(1, 2)
            
            # Fill case number
            case_number_input = self.driver.find_element(By.ID, "case_number")
            case_number_input.clear()
            case_number_input.send_keys(case_number)
            logger.info(f"Filled case number: {case_number}")
            self.random_delay(1, 2)
            
            # Fill filing year dropdown
            case_year_select = self.driver.find_element(By.ID, "case_year")
            select_case_year = Select(case_year_select)
            select_case_year.select_by_value(filing_year)
            logger.info(f"Selected filing year: {filing_year}")
            self.random_delay(1, 2)

            # Get and fill captcha
            captcha_code = self.get_captcha_code()
            if captcha_code:
                captcha_input = self.driver.find_element(By.ID, "captchaInput")
                captcha_input.clear()
                captcha_input.send_keys(captcha_code)
                logger.info(f"Filled captcha code: {captcha_code}")
                self.random_delay(1, 2)
            else:
                logger.warning("Could not get captcha code")
            
        except Exception as e:
            logger.error(f"Error filling search form: {e}")
            raise
    
    def submit_search_form(self):
        """Submit the search form"""
        try:
            # Find and click the submit button
            submit_btn = self.driver.find_element(By.ID, "search")
            submit_btn.click()
            logger.info("Clicked submit button")
            self.random_delay(3, 5)  # Reduced delay for production
            return True
            
        except Exception as e:
            logger.error(f"Error submitting search form: {e}")
            return False
    
    def extract_case_data(self):
        """Extract case information from search results"""
        try:
            logger.info("Extracting case data from search results...")
            
            # Wait for results table to load
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, "caseTable")))
                logger.info("Results table found")
            except TimeoutException:
                logger.warning("No results table found, case might not exist")
                return None
            
            # Check if case was found by looking for table rows
            table = self.driver.find_element(By.ID, "caseTable")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            if not rows:
                logger.warning("No case data found in table")
                return None
            
            # Extract case information from the table
            case_data = {
                "parties": self.extract_parties_from_table(rows),
                "dates": self.extract_dates_from_table(rows),
                "order_page_link": self.extract_orders_from_table(rows),
                "case_status": self.extract_case_status_from_table(rows)
            }

            logger.info("Successfully extracted case data")
            return case_data
            
        except Exception as e:
            logger.error(f"Error extracting case data: {e}")
            return None
    

    def extract_parties_from_table(self, rows):
        """Extract petitioner and respondent information from table rows"""
        try:
            parties = {"petitioner": "N/A", "respondent": "N/A"}
            
            if rows:
                # Get the first row (most recent case)
                first_row = rows[0]
                cells = first_row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 3:  # Should have at least 3 columns
                    # The third column contains "Petitioner VS. Respondent"
                    party_cell = cells[2]
                    party_text = party_cell.text.strip()
                    
                    # Handle the format: "AATMNIRBHAR INFRATECH PVT. LTD. AND ANR.\nVS.\nYASH PAL BATRA AND ORS."
                    if "VS." in party_text:
                        parts = party_text.split("VS.")
                        if len(parts) >= 2:
                            petitioner = parts[0].strip()
                            respondent = parts[1].strip()
                            # Clean up any extra whitespace and newlines
                            parties["petitioner"] = petitioner.replace('\n', ' ').strip()
                            parties["respondent"] = respondent.replace('\n', ' ').strip()
                    else:
                        parties["petitioner"] = party_text.replace('\n', ' ').strip()
            
            return parties
            
        except Exception as e:
            logger.error(f"Error extracting parties from table: {e}")
            return {"petitioner": "N/A", "respondent": "N/A"}
    

    def extract_dates_from_table(self, rows):
        """Extract filing and hearing dates from table rows"""
        try:
            dates = {"filing_date": "N/A", "next_hearing": "N/A"}
            
            if rows:
                # Get the first row (most recent case)
                first_row = rows[0]
                cells = first_row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 4:  # Should have at least 4 columns
                    # The fourth column contains "NEXT DATE: 11/08/2025\nLast Date: 13/05/2025\nCOURT NO:41"
                    date_cell = cells[3]
                    date_text = date_cell.text.strip()
                    
                    if date_text and date_text != "":
                        # Parse the date information
                        lines = date_text.split('\n')

                        for line in lines:
                            line = line.strip()
                            if line.startswith("NEXT DATE:"):
                                next_date = line.replace("NEXT DATE:", "").strip()
                                dates["next_hearing"] = next_date
                            elif line.startswith("Last Date:"):
                                last_date = line.replace("Last Date:", "").strip()
                                dates["filing_date"] = last_date
                            elif line.startswith("COURT NO:"):
                                court_no = line.replace("COURT NO:", "").strip()
                                dates["court_no"] = court_no
                    else:
                        dates["next_hearing"] = "No hearing date available"
            
            return dates
            
        except Exception as e:
            logger.error(f"Error extracting dates from table: {e}")
            return {"filing_date": "N/A", "next_hearing": "N/A"}
    

    def extract_orders_from_table(self, rows):
        """Extract order link"""
        try:
            
            if rows:
                first_row = rows[0]
                cells = first_row.find_elements(By.TAG_NAME, "td")

              
                if len(cells) >= 2:  # Should have at least 2 columns
                    case_cell = cells[1]

                    try:
                      
                        order_link = case_cell.find_element("xpath", "//*[@id='caseTable']/tbody/tr/td[2]/a[2]").get_attribute("href")

                        return order_link

                     
                    except NoSuchElementException:
                        pass
                    
          
            return '#'
            
        except Exception as e:
            logger.error(f"Error extracting orders from table: {e}")
            return '#'


        
    def get_latest_order_pdf_link(self, order_page_link):

        if order_page_link == '#':
            return '#'
        
        """Extract order link, navigate, and get target link"""
        try:
            logger.info("Getting latest order pdf link")

            self.driver.get(order_page_link)

            self.random_delay(1, 2)

            # Wait for page to load and form to be present
            self.wait.until(EC.presence_of_element_located((By.ID, "caseTable")))

            target_link = self.driver.find_element(
                By.XPATH, "//*[@id='caseTable']/tbody/tr[1]/td[2]/a"
            ).get_attribute("href")

            return target_link

            

        except Exception as e:
            logger.error(f"Error extracting orders from table: {e}")
            return '#'






    
    def extract_case_status_from_table(self, rows):
        """Extract case status from table rows"""
        try:
            if rows:
                # Get the first row (most recent case)
                first_row = rows[0]
                cells = first_row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 2:  # Should have at least 2 columns
                    # The second column contains case info with status in green font
                    case_cell = cells[1]
                    
                    # Look for status in font tag with green color
                    try:
                        status_font = case_cell.find_element(By.TAG_NAME, "font")
                        if status_font and status_font.get_attribute("color") == "green":
                            status = status_font.text.strip()
                            # Remove brackets if present
                            if status.startswith("[") and status.endswith("]"):
                                status = status[1:-1]
                            return status
                    except NoSuchElementException:
                        pass
                    
                    # Fallback: extract from text content
                    case_text = case_cell.text.strip()
                    if "[" in case_text and "]" in case_text:
                        status_start = case_text.find("[") + 1
                        status_end = case_text.find("]")
                        status = case_text[status_start:status_end]
                        return status
                    else:
                        return "Active"
            
            return "Pending"
            
        except Exception as e:
            logger.error(f"Error extracting case status from table: {e}")
            return "Pending"
    
    def scrape_case(self, case_type, case_number, filing_year):
        """Main method to scrape case information"""
        try:
            logger.info(f"Starting case scrape: {case_type}/{case_number}/{filing_year}")
            
            # Setup driver
            self.setup_driver()
            
            # Navigate to website
            self.navigate_to_court_website()
            
            # Fill search form
            self.fill_case_search_form(case_type, case_number, filing_year)
            
            # Submit form
            if not self.submit_search_form():
                logger.warning("Could not submit search form, using mock data")
                return self.create_mock_data(case_type, case_number, filing_year), "Mock data - submit failed"
            
            # Extract data
            case_data = self.extract_case_data()
            
            if case_data:
                # Add case metadata
                case_data.update({
                    "case_type": case_type,
                    "case_number": case_number,
                    "pdf_link": self.get_latest_order_pdf_link(case_data['order_page_link'])
                })

                logger.info("Case data extracted successfully")
                
                return case_data, self.driver.page_source
            else:
                logger.warning("No case data extracted, using mock data")
                return self.create_mock_data(case_type, case_number, filing_year), "Mock data - extraction failed"
                
        except Exception as e:
            logger.error(f"Error during case scraping: {e}")
            return self.create_mock_data(case_type, case_number, filing_year), f"Mock data - error: {str(e)}"
        finally:
            if self.driver:
                self.driver.quit()
    
    def create_mock_data(self, case_type, case_number, filing_year):
        """Create mock data for demonstration purposes"""
        return {
            "parties": {
                "petitioner": f"Petitioner for {case_number}",
                "respondent": f"Respondent for {case_number}"
            },
            "dates": {
                "filing_date": f"{filing_year}-01-15",
                "next_hearing": f"{filing_year}-12-20"
            },
            "orders": [
                {
                    "date": f"{filing_year}-11-15",
                    "title": "Latest Order",
                    "pdf_url": f"/orders/{case_number}_latest.pdf"
                }
            ],
            "case_status": "Pending",
            "case_type": case_type,
            "case_number": case_number
        }

# Convenience function for external use
def scrape_delhi_high_court(case_type, case_number, filing_year, headless=True):
    """
    Convenience function to scrape Delhi High Court case information
    
    Args:
        case_type (str): Type of case (WP, CRL, etc.)
        case_number (str): Case number
        filing_year (str): Filing year
        headless (bool): Run browser in headless mode (default: True for production)
    
    Returns:
        tuple: (parsed_data, raw_response)
    """
    scraper = DelhiHighCourtScraper(headless=headless)
    return scraper.scrape_case(case_type, case_number, filing_year)
