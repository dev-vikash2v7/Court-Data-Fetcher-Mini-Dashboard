from flask import Flask, render_template, request, jsonify, send_file
from scraper import scrape_delhi_high_court
import sqlite3
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)

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

# The scraping functionality is now handled by the scraper.py module

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch-case', methods=['POST'])
def fetch_case():
    try:
        data = request.get_json()
        case_type = data.get('caseType')
        case_number = data.get('caseNumber')
        filing_year = data.get('filingYear')
        
        if not all([case_type, case_number, filing_year]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Scrape the court website
        parsed_data, raw_response = scrape_delhi_high_court(case_type, case_number, filing_year)
        
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
    try:
        data = request.get_json()
        pdf_url = data.get('pdfUrl')
        
        if not pdf_url:
            return jsonify({'error': 'PDF URL is required'}), 400
        
        # In a real implementation, you would download the PDF from the court website
        # For now, we'll return a mock response
        return jsonify({
            'success': True,
            'message': f'PDF download initiated for: {pdf_url}',
            'downloadUrl': pdf_url
        })
        
    except Exception as e:
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
