from flask import Flask, render_template_string
import requests

app = Flask(__name__)

APPLICATION_NUMBERS = [
    "1912022811593", "1912021168726"  # Add more numbers here
]

API_URL = "https://pmfme.mofpi.gov.in/mofpi/api/users/getApplicationStatus/{}/applicationNumber"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36"
}

def fetch_status(application_number):
    response = requests.post(API_URL.format(application_number), headers=HEADERS, json={})
    return response.json() if response.status_code == 200 else None

@app.route("/")
def index():
    results = [fetch_status(app_no) for app_no in APPLICATION_NUMBERS]
    return render_template_string(TEMPLATE, results=results)

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Application Status</title>
    <style>
        table { width: 100%%; border-collapse: collapse; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Application Status</h2>
    <table>
        <tr>
            <th>Application Number</th>
            <th>Name</th>
            <th>State</th>
            <th>District</th>
            <th>Category</th>
            <th>Current Status</th>
        </tr>
        {% for result in results %}
            {% if result %}
            <tr>
                <td>{{ result['responseObject']['applicationNumber'] }}</td>
                <td>{{ result['responseObject']['name'] }}</td>
                <td>{{ result['responseObject']['state'] }}</td>
                <td>{{ result['responseObject']['district'] }}</td>
                <td>{{ result['responseObject']['category'] }}</td>
                <td>{{ result['responseObject']['currentStatus'] }}</td>
            </tr>
            {% endif %}
        {% endfor %}
    </table>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
