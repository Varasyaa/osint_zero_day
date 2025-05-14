from flask import Flask, request, jsonify, render_template
import requests
import pymongo
import os

app = Flask(__name__)

# Load API Keys from environment or hardcode for testing
VT_API_KEY = os.getenv("VT_API_KEY", "YOUR_VIRUSTOTAL_KEY")
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "YOUR_SHODAN_KEY")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["osint_db"]
collection = db["scans"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def check_ip():
    data = request.get_json()
    target = data['ip']
    vt_url = f"https://www.virustotal.com/api/v3/ip_addresses/{target}"
    vt_headers = {"x-apikey": VT_API_KEY}
    vt_resp = requests.get(vt_url, headers=vt_headers)
    vt_data = vt_resp.json()

    stats = vt_data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
    result = {
        "status": "Scanned successfully",
        "data": {
            "harmless": stats.get("harmless", 0),
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0)
        }
    }

    # Save to DB
    collection.insert_one({
        "target": target,
        "result": result["data"]
    })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
