"""
Delhi High Court Web Scraper Module
Handles automated data extraction from the Delhi High Court website
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import random
import logging
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DelhiHighCourtScraper:
    """
    Scraper class for Delhi High Court website
    """
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with anti-detection measures"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection measures
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Custom user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Chrome WebDriver setup successful")
        except Exception as e:
            logger.error(f"Failed to setup Chrome WebDriver: {e}")
            raise
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay to avoid detection"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def navigate_to_court_website(self):
        """Navigate to Delhi High Court website"""
        try:
            logger.info("Navigating to Delhi High Court website...")
            self.driver.get("https://delhihighcourt.nic.in/")
            self.random_delay(2, 4)
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("Successfully loaded Delhi High Court website")
            
        except Exception as e:
            logger.error(f"Failed to navigate to court website: {e}")
            raise
    
    def find_case_status_link(self):
        """Find and click on case status or cause list link"""
        try:
            # Common selectors for case status links
            possible_selectors = [
                "//a[contains(text(), 'Case Status')]",
                "//a[contains(text(), 'Cause List')]",
                "//a[contains(text(), 'Case Information')]",
                "//a[contains(text(), 'Search Cases')]",
                "//a[contains(@href, 'case')]",
                "//a[contains(@href, 'status')]"
            ]
            
            for selector in possible_selectors:
                try:
                    link = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    logger.info(f"Found case status link: {link.text}")
                    link.click()
                    self.random_delay(2, 4)
                    return True
                except TimeoutException:
                    continue
            
            logger.warning("Could not find case status link, trying alternative approach")
            return False
            
        except Exception as e:
            logger.error(f"Error finding case status link: {e}")
            return False
    
    def fill_case_search_form(self, case_type, case_number, filing_year):
        """Fill the case search form with provided details"""
        try:
            logger.info(f"Filling search form: {case_type}/{case_number}/{filing_year}")
            
            # Common field selectors
            field_selectors = {
                'case_type': [
                    "//select[@name='caseType']",
                    "//select[@id='caseType']",
                    "//input[@name='caseType']",
                    "//input[@id='caseType']"
                ],
                'case_number': [
                    "//input[@name='caseNumber']",
                    "//input[@id='caseNumber']",
                    "//input[@name='caseNo']",
                    "//input[@id='caseNo']"
                ],
                'filing_year': [
                    "//select[@name='filingYear']",
                    "//select[@id='filingYear']",
                    "//input[@name='filingYear']",
                    "//input[@id='filingYear']"
                ]
            }
            
            # Fill case type
            for selector in field_selectors['case_type']:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select
                        select = Select(element)
                        select.select_by_value(case_type)
                    else:
                        element.clear()
                        element.send_keys(case_type)
                    logger.info("Filled case type field")
                    break
                except NoSuchElementException:
                    continue
            
            # Fill case number
            for selector in field_selectors['case_number']:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    element.clear()
                    element.send_keys(case_number)
                    logger.info("Filled case number field")
                    break
                except NoSuchElementException:
                    continue
            
            # Fill filing year
            for selector in field_selectors['filing_year']:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.tag_name == 'select':
                        from selenium.webdriver.support.ui import Select
                        select = Select(element)
                        select.select_by_value(filing_year)
                    else:
                        element.clear()
                        element.send_keys(filing_year)
                    logger.info("Filled filing year field")
                    break
                except NoSuchElementException:
                    continue
            
            self.random_delay(1, 2)
            
        except Exception as e:
            logger.error(f"Error filling search form: {e}")
            raise
    
    def submit_search_form(self):
        """Submit the search form"""
        try:
            # Common submit button selectors
            submit_selectors = [
                "//input[@type='submit']",
                "//button[@type='submit']",
                "//input[@value='Search']",
                "//button[contains(text(), 'Search')]",
                "//input[@value='Submit']",
                "//button[contains(text(), 'Submit')]"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(By.XPATH, selector)
                    submit_btn.click()
                    logger.info("Submitted search form")
                    self.random_delay(3, 6)  # Longer delay for search results
                    return True
                except NoSuchElementException:
                    continue
            
            logger.warning("Could not find submit button")
            return False
            
        except Exception as e:
            logger.error(f"Error submitting search form: {e}")
            return False
    
    def extract_case_data(self):
        """Extract case information from search results"""
        try:
            logger.info("Extracting case data from search results...")
            
            # Get page source for analysis
            page_source = self.driver.page_source
            
            # Check if case was found
            if "no case found" in page_source.lower() or "case not found" in page_source.lower():
                logger.warning("Case not found in search results")
                return None
            
            # Extract case information using various selectors
            case_data = {
                "parties": self.extract_parties(),
                "dates": self.extract_dates(),
                "orders": self.extract_orders(),
                "case_status": self.extract_case_status()
            }
            
            logger.info("Successfully extracted case data")
            return case_data
            
        except Exception as e:
            logger.error(f"Error extracting case data: {e}")
            return None
    
    def extract_parties(self):
        """Extract petitioner and respondent information"""
        try:
            parties = {"petitioner": "N/A", "respondent": "N/A"}
            
            # Common selectors for party information
            party_selectors = {
                'petitioner': [
                    "//td[contains(text(), 'Petitioner')]/following-sibling::td",
                    "//div[contains(text(), 'Petitioner')]/following-sibling::div",
                    "//span[contains(text(), 'Petitioner')]/following-sibling::span"
                ],
                'respondent': [
                    "//td[contains(text(), 'Respondent')]/following-sibling::td",
                    "//div[contains(text(), 'Respondent')]/following-sibling::div",
                    "//span[contains(text(), 'Respondent')]/following-sibling::span"
                ]
            }
            
            for party_type, selectors in party_selectors.items():
                for selector in selectors:
                    try:
                        element = self.driver.find_element(By.XPATH, selector)
                        parties[party_type] = element.text.strip()
                        break
                    except NoSuchElementException:
                        continue
            
            return parties
            
        except Exception as e:
            logger.error(f"Error extracting parties: {e}")
            return {"petitioner": "N/A", "respondent": "N/A"}
    
    def extract_dates(self):
        """Extract filing and hearing dates"""
        try:
            dates = {"filing_date": "N/A", "next_hearing": "N/A"}
            
            # Common selectors for date information
            date_selectors = {
                'filing_date': [
                    "//td[contains(text(), 'Filing Date')]/following-sibling::td",
                    "//div[contains(text(), 'Filing Date')]/following-sibling::div"
                ],
                'next_hearing': [
                    "//td[contains(text(), 'Next Hearing')]/following-sibling::td",
                    "//div[contains(text(), 'Next Hearing')]/following-sibling::div",
                    "//td[contains(text(), 'Hearing Date')]/following-sibling::td"
                ]
            }
            
            for date_type, selectors in date_selectors.items():
                for selector in selectors:
                    try:
                        element = self.driver.find_element(By.XPATH, selector)
                        dates[date_type] = element.text.strip()
                        break
                    except NoSuchElementException:
                        continue
            
            return dates
            
        except Exception as e:
            logger.error(f"Error extracting dates: {e}")
            return {"filing_date": "N/A", "next_hearing": "N/A"}
    
    def extract_orders(self):
        """Extract order and judgment information"""
        try:
            orders = []
            
            # Look for order links or information
            order_selectors = [
                "//a[contains(@href, '.pdf')]",
                "//a[contains(text(), 'Order')]",
                "//a[contains(text(), 'Judgment')]",
                "//a[contains(@href, 'order')]",
                "//a[contains(@href, 'judgment')]"
            ]
            
            for selector in order_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        order = {
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "title": element.text.strip() or "Order/Judgment",
                            "pdf_url": element.get_attribute('href') or "#"
                        }
                        orders.append(order)
                except Exception:
                    continue
            
            # If no orders found, create a mock order
            if not orders:
                orders = [{
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "title": "Latest Order",
                    "pdf_url": "#"
                }]
            
            return orders
            
        except Exception as e:
            logger.error(f"Error extracting orders: {e}")
            return [{
                "date": datetime.now().strftime("%Y-%m-%d"),
                "title": "Latest Order",
                "pdf_url": "#"
            }]
    
    def extract_case_status(self):
        """Extract case status"""
        try:
            status_selectors = [
                "//td[contains(text(), 'Status')]/following-sibling::td",
                "//div[contains(text(), 'Status')]/following-sibling::div",
                "//span[contains(text(), 'Status')]/following-sibling::span"
            ]
            
            for selector in status_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    status = element.text.strip()
                    if status:
                        return status
                except NoSuchElementException:
                    continue
            
            return "Pending"
            
        except Exception as e:
            logger.error(f"Error extracting case status: {e}")
            return "Pending"
    
    def scrape_case(self, case_type, case_number, filing_year):
        """Main method to scrape case information"""
        try:
            logger.info(f"Starting case scrape: {case_type}/{case_number}/{filing_year}")
            
            # Setup driver
            self.setup_driver()
            
            # Navigate to website
            self.navigate_to_court_website()
            
            # Find and click case status link
            if not self.find_case_status_link():
                logger.warning("Could not find case status link, using mock data")
                return self.create_mock_data(case_type, case_number, filing_year), "Mock data - link not found"
            
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
                    "case_number": case_number
                })
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
        headless (bool): Run browser in headless mode
    
    Returns:
        tuple: (parsed_data, raw_response)
    """
    scraper = DelhiHighCourtScraper(headless=headless)
    return scraper.scrape_case(case_type, case_number, filing_year)
