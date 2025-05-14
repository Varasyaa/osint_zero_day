import os
import requests
from flask import Blueprint, request, jsonify
from pymongo import MongoClient

shodan_bp = Blueprint('shodan_bp', __name__)
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY') or "your_shodan_api_key_here"

client = MongoClient("mongodb://localhost:27017/")
db = client.osint
shodan_collection = db.shodan_results

@shodan_bp.route('/api/shodan', methods=['POST'])
def shodan_search():
    data = request.get_json()
    target = data.get("target")
    if not target:
        return jsonify({"error": "Target required"}), 400

    url = f"https://api.shodan.io/shodan/host/{target}?key={SHODAN_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Shodan lookup failed"}), 500

    result = response.json()
    result["target"] = target
    shodan_collection.insert_one(result)
    return jsonify(result)
