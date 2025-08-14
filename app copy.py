from flask import Flask, render_template, request, jsonify, send_file
from scraper import scrape_delhi_high_court
import sqlite3
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)

# Production configuration
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
else:
    # For production deployment
    app.config['DEBUG'] = False

# Database setup
def init_db():
    conn = sqlite3.connect('court_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            filing_year TEXT,
            query_timestamp DATETIME,
            raw_response TEXT,
            parsed_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_query(case_type, case_number, filing_year, raw_response, parsed_data):
    conn = sqlite3.connect('court_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO queries (case_type, case_number, filing_year, query_timestamp, raw_response, parsed_data)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (case_type, case_number, filing_year, datetime.now(), raw_response, json.dumps(parsed_data)))
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/fetch-case', methods=['POST'])
def fetch_case():
    try:
        print("fetching case")
        data = request.get_json()
        case_type = data.get('caseType')
        case_number = data.get('caseNumber')
        filing_year = data.get('filingYear')
        
        if not all([case_type, case_number, filing_year]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Scrape the court website (headless mode for production)
        parsed_data, raw_response = scrape_delhi_high_court(case_type, case_number, filing_year, headless=True)
        
        if parsed_data is None:
            return jsonify({'error': f'Failed to fetch case data: {raw_response}'}), 500
        
        # Log the query
        log_query(case_type, case_number, filing_year, raw_response, parsed_data)
        
        return jsonify({
            'success': True,
            'data': parsed_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/download-pdf', methods=['POST'])
def download_pdf():

    data = request.get_json()
    pdf_url = data.get('pdfUrl')
    filename = data.get('filename')

    
    try:
        # Send a GET request to the URL
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        download_directory = ".\downloads"  # Replace with your desired path
        save_path = os.path.join(download_directory, filename) 

        # Open the local file in binary write mode
        with open(save_path, 'wb') as pdf_file:
            # Iterate over the response content in chunks to handle large files
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)


        print(f"PDF downloaded successfully to: {save_path}")

        return jsonify({
            'success': True,
            'message': f'PDF downloaded successfully to: Project/downloads/{filename}'
        })

    except Exception as e:
        print('error' , e)
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/api/query-history')
def query_history():
    try:
        conn = sqlite3.connect('court_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT case_type, case_number, filing_year, query_timestamp 
            FROM queries 
            ORDER BY query_timestamp DESC 
            LIMIT 10
        ''')
        history = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'history': [
                {
                    'caseType': row[0],
                    'caseNumber': row[1],
                    'filingYear': row[2],
                    'timestamp': row[3]
                }
                for row in history
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch history: {str(e)}'}), 500
