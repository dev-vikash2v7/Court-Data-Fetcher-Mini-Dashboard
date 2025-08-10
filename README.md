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
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with modern design principles

## Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
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

**Request Body:**
```json
{
    "caseType": "WP",
    "caseNumber": "12345",
    "filingYear": "2023"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "case_type": "WP",
        "case_number": "12345",
        "case_status": "Pending",
        "parties": {
            "petitioner": "Petitioner Name",
            "respondent": "Respondent Name"
        },
        "dates": {
            "filing_date": "2023-01-15",
            "next_hearing": "2023-12-20"
        },
        "orders": [
            {
                "date": "2023-11-15",
                "title": "Latest Order",
                "pdf_url": "/orders/12345_latest.pdf"
            }
        ]
    }
}
```

### POST /api/download-pdf
Initiates PDF download for court orders.

**Request Body:**
```json
{
    "pdfUrl": "/orders/12345_latest.pdf"
}
```

### GET /api/query-history
Retrieves recent search history.

**Response:**
```json
{
    "success": true,
    "history": [
        {
            "caseType": "WP",
            "caseNumber": "12345",
            "filingYear": "2023",
            "timestamp": "2023-12-01T10:30:00"
        }
    ]
}
```

## Web Scraping Approach

The application uses Selenium WebDriver to:

1. **Navigate** to the Delhi High Court website
2. **Bypass** view-state tokens and CAPTCHA challenges
3. **Fill** search forms with case details
4. **Extract** case information including:
   - Party names (petitioner/respondent)
   - Filing and hearing dates
   - Case status
   - Order/judgment PDF links
5. **Parse** and structure the data for display

### Anti-Detection Measures

- Headless browser mode
- Custom user agent strings
- Random delays between requests
- Session management
- Error handling for CAPTCHA challenges

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

## Configuration

### Environment Variables

You can configure the application using environment variables:

- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_DEBUG`: Enable/disable debug mode
- `DATABASE_URL`: Custom database URL (defaults to SQLite)

### Chrome WebDriver Configuration

The application automatically configures Chrome WebDriver with:

- Headless mode for server deployment
- Disabled GPU acceleration
- Custom window size
- User agent spoofing
- Security sandbox disabled

## Error Handling

The application includes comprehensive error handling:

- **Network errors**: Retry mechanisms and user notifications
- **Invalid case numbers**: Validation and helpful error messages
- **Website changes**: Graceful degradation and logging
- **CAPTCHA challenges**: Detection and user guidance
- **Database errors**: Connection management and recovery

## Security Considerations

- Input validation and sanitization
- SQL injection prevention using parameterized queries
- XSS protection through proper output encoding
- Rate limiting for API endpoints
- Secure session management

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure reverse proxy (Nginx, Apache)
4. Set up SSL/TLS certificates
5. Configure database backups

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for educational and research purposes. Please ensure compliance with the Delhi High Court's terms of service and applicable laws when using this tool. The developers are not responsible for any misuse of this application.

## Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include error logs and system information

## Roadmap

- [ ] Support for additional courts
- [ ] Advanced search filters
- [ ] Email notifications for case updates
- [ ] Mobile application
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Multi-language support
