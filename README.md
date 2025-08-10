# Court Data Fetcher - Delhi High Court

A Flask-based web application for fetching and displaying case information from the Delhi High Court website using Selenium web scraping.

## Features

- **Case Search**: Search for cases by Case Type, Case Number, and Filing Year
- **Web Scraping**: Automated data extraction from Delhi High Court website using Selenium
- **Data Storage**: SQLite database for logging queries and responses
- **Modern UI**: Clean, responsive interface with real-time updates
- **PDF Downloads**: Download court orders and judgments
- **Search History**: Track and reuse previous searches
- **Error Handling**: User-friendly error messages and validation

## Technology Stack

- **Backend**: Python Flask
- **Web Scraping**: Selenium WebDriver
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript 
- **Styling**: Custom CSS with modern design principles

## Prerequisites

- Python 3.8 or higher
- Latest Chrome browser (for Selenium WebDriver)
- ChromeDriver (will be automatically managed by Selenium)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd court-data-fetcher
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
court-data-fetcher/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── court_data.db         # SQLite database (created automatically)
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Custom stylesheets
    └── js/
        └── app.js        # Frontend JavaScript
```

## API Endpoints

### POST /api/fetch-case
Fetches case information from Delhi High Court website.



## Database Schema

The SQLite database (`court_data.db`) contains a single table:

```sql
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_type TEXT,
    case_number TEXT,
    filing_year TEXT,
    query_timestamp DATETIME,
    raw_response TEXT,
    parsed_data TEXT
);
```
## Build and start the Docker services

```docker-compose up --build```
