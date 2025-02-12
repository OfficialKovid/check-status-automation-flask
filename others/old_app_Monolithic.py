from flask import Flask, render_template_string, jsonify
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

@app.route("/refresh/<application_number>")
def refresh(application_number):
    result = fetch_status(application_number)
    return jsonify(result)

@app.route("/refresh-all")
def refresh_all():
    results = [fetch_status(app_no) for app_no in APPLICATION_NUMBERS]
    return jsonify(results)

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Application Status</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 20px; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #007BFF; color: white; }
        .status-cell { font-weight: bold; padding: 10px; border-radius: 4px; }
        button { margin: 10px 0; padding: 10px; font-size: 16px; background: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .blur { filter: blur(5px); }
        .loading { text-align: center; font-size: 18px; display: none; }
    </style>
    <script>
        function refreshAllData() {
            document.getElementById("table-body").classList.add("blur");
            document.getElementById("loading").style.display = "block";
            fetch('/refresh-all')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("table-body").classList.remove("blur");
                    document.getElementById("loading").style.display = "none";
                    updateTable(data);
                });
        }

        function refreshRow(applicationNumber, button) {
            let row = button.closest("tr");
            row.classList.add("blur");
            fetch(`/refresh/${applicationNumber}`)
                .then(response => response.json())
                .then(result => {
                    row.classList.remove("blur");
                    updateRow(row, result);
                });
        }

        function updateTable(data) {
            let tableBody = document.getElementById('table-body');
            tableBody.innerHTML = '';
            data.forEach(result => {
                if (result) {
                    let row = createRow(result);
                    tableBody.innerHTML += row;
                }
            });
        }

        function updateRow(row, result) {
            row.innerHTML = createRowContent(result);
        }

        function createRow(result) {
            return `<tr>${createRowContent(result)}</tr>`;
        }

        function createRowContent(result) {
            return `
                <td>${result.responseObject.applicationNumber}</td>
                <td>${result.responseObject.userId.trim()}</td>
                <td>${result.responseObject.name}</td>
                <td>${result.responseObject.state}</td>
                <td>${result.responseObject.district}</td>
                <td>${result.responseObject.category}</td>
                <td>${result.responseObject.subCategory}</td>
                <td>${result.responseObject.submitTime || 'N/A'}</td>
                <td style="background-color: ${result.responseObject.bgColor}; color: ${result.responseObject.color}" class="status-cell">${result.responseObject.currentStatus}</td>
                <td><button onclick="refreshRow('${result.responseObject.applicationNumber}', this)">Refresh</button></td>`;
        }
    </script>
</head>
<body>
    <h2>Application Status</h2>
    <button onclick="refreshAllData()">Refresh / Recheck All</button>
    <div id="loading" class="loading">Loading...</div>
    <table>
        <tr>
            <th>Application Number</th>
            <th>User ID</th>
            <th>Name</th>
            <th>State</th>
            <th>District</th>
            <th>Category</th>
            <th>Sub Category</th>
            <th>Submission Date</th>
            <th>Current Status</th>
            <th>Actions</th>
        </tr>
        <tbody id="table-body">
        {% for result in results %}
            {% if result %}
            <tr>
                <td>{{ result['responseObject']['applicationNumber'] }}</td>
                <td>{{ result['responseObject']['userId'].strip() }}</td>
                <td>{{ result['responseObject']['name'] }}</td>
                <td>{{ result['responseObject']['state'] }}</td>
                <td>{{ result['responseObject']['district'] }}</td>
                <td>{{ result['responseObject']['category'] }}</td>
                <td>{{ result['responseObject']['subCategory'] }}</td>
                <td>{{ result['responseObject']['submitTime'] if result['responseObject']['submitTime'] else 'N/A' }}</td>
                <td style="background-color: {{ result['responseObject']['bgColor'] }}; color: {{ result['responseObject']['color'] }}" class="status-cell">{{ result['responseObject']['currentStatus'] }}</td>
                <td><button onclick="refreshRow('{{ result['responseObject']['applicationNumber'] }}', this)">Refresh</button></td>
            </tr>
            {% endif %}
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
