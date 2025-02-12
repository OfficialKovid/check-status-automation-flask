from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime
from output_list import APPLICATION_NUMBERS

app = Flask(__name__)

STATUS_COLORS = {
    'SUBMITTED': {'bg': '#FEF3C7', 'text': '#92400E'},
    'APPROVED': {'bg': '#D1FAE5', 'text': '#065F46'},
    'REJECTED': {'bg': '#FEE2E2', 'text': '#991B1B'},
    'PROCESSING': {'bg': '#DBEAFE', 'text': '#1E40AF'}
}


def make_curl_request(application_number):
    url = f'https://pmfme.mofpi.gov.in/mofpi/api/users/getApplicationStatus/{application_number}/applicationNumber'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://pmfme.mofpi.gov.in',
        'Referer': 'https://pmfme.mofpi.gov.in/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching status for {application_number}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status/<application_number>')
def get_status(application_number):
    result = make_curl_request(str(application_number))
    return jsonify(result)

@app.route('/api/batch-status')
def get_batch_status():
    results = []
    for number in APPLICATION_NUMBERS:
        result = make_curl_request(str(number))
        if result:
            results.append(result)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)