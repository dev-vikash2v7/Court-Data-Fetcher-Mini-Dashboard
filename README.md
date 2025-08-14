# Delhi High Court Case Scraper

A web application for scraping and retrieving case information from the Delhi High Court website.

## Features

- Search cases by case type, case number, and filing year
- Extract case details including parties, dates, and status
- Download case orders and documents
- Production-ready with headless Chrome support
- Deployable on Render, Heroku, and other cloud platforms

## Production Deployment

### Deploy on Render (Recommended)

1. **Fork/Clone this repository**
2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration

3. **Automatic Deployment:**
   - The service will be automatically deployed using the configuration in `render.yaml`
   - Chrome and all dependencies will be installed automatically
   - The application will run in headless mode for production

### Manual Render Deployment

If you prefer manual setup:

1. Create a new Web Service on Render
2. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --config gunicorn.conf.py app:app`
   - **Environment Variables:**
     - `PORT`: `5000`
     - `PYTHON_VERSION`: `3.9.0`

### Docker Deployment

```bash
# Build the Docker image
docker build -t court-scraper .

# Run the container
docker run -p 5000:5000 court-scraper
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## API Endpoints

### POST /api/fetch-case
Search for a case by providing case details.

**Request Body:**
```json
{
  "caseType": "WP",
  "caseNumber": "1234",
  "filingYear": "2024"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "case_type": "WP",
    "case_number": "1234",
    "parties": {
      "petitioner": "Petitioner Name",
      "respondent": "Respondent Name"
    },
    "dates": {
      "filing_date": "2024-01-15",
      "next_hearing": "2024-12-20"
    },
    "case_status": "Pending",
    "pdf_link": "https://..."
  }
}
```

### POST /api/download-pdf
Download a PDF file from a URL.

**Request Body:**
```json
{
  "pdfUrl": "https://example.com/document.pdf",
  "filename": "document.pdf"
}
```

## Technical Details

### Production Features

- **Headless Chrome:** Runs without GUI for server deployment
- **Gunicorn:** Production WSGI server
- **Anti-detection:** Chrome options to avoid bot detection
- **Error Handling:** Comprehensive error handling and logging
- **Database:** SQLite for query logging
- **Caching:** Optimized for performance

### Chrome Configuration

The scraper uses the following Chrome options for production:

```python
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-images')
chrome_options.add_argument('--disable-javascript')
```

### Environment Variables

- `PORT`: Application port (default: 5000)
- `PYTHON_VERSION`: Python version (default: 3.9.0)

## Troubleshooting

### Common Issues

1. **Chrome not found:** Ensure Chrome is installed in the Docker container
2. **Timeout errors:** Increase timeout values in the scraper
3. **Memory issues:** Reduce worker count in gunicorn.conf.py
4. **Captcha issues:** The scraper handles captcha automatically

### Logs

Check application logs for debugging:
- Render: View logs in the Render dashboard
- Docker: `docker logs <container_id>`
- Local: Check console output

## License

This project is for educational purposes only. Please respect the Delhi High Court website's terms of service.
