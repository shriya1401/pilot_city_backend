import json
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with proper settings
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://127.0.0.1:4887"}})

# Define the Blueprint
search_api = Blueprint('search_api', __name__)

# File to save items data
DATA_FILE = "items_data.json"

# Load items from the JSON file, or use default items if the file doesn't exist
def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return [
        {"name": "Teddy Bear", "link": "holiday/toys", "tags": {"all": 1, "teddy": 0, "bear": 0, "toys": 0}},
        {"name": "Lego Set", "link": "holiday/toys", "tags": {"all": 1, "lego": 0, "set": 0, "toys": 0}},
        {"name": "Remote Control Car", "link": "holiday/toys", "tags": {"all": 1, "remote": 0, "control": 0, "car": 0, "toys": 0}},
        {"name": "Holiday Candles", "link": "holiday/home-decor", "tags": {"all": 1, "holiday": 0, "candles": 0, "home-decor": 0}},
        {"name": "Festive Wreath", "link": "holiday/home-decor", "tags": {"all": 1, "festive": 0, "wreath": 0, "home-decor": 0}},
        {"name": "Decorative Ornaments", "link": "holiday/home-decor", "tags": {"all": 1, "decorative": 0, "ornaments": 0, "home-decor": 0}},
        {"name": "Wireless Headphones", "link": "holiday/electronics", "tags": {"all": 1, "wireless": 0, "headphones": 0, "electronics": 0}},
        {"name": "Smartwatch", "link": "holiday/electronics", "tags": {"all": 1, "smartwatch": 0, "electronics": 0}},
        {"name": "Gaming Console", "link": "holiday/electronics", "tags": {"all": 1, "gaming": 0, "console": 0, "electronics": 0}},
        {"name": "Cozy Holiday Sweater", "link": "holiday/clothes", "tags": {"all": 1, "cozy": 0, "holiday": 0, "sweater": 0, "clothes": 0}},
        {"name": "Woolen Scarf", "link": "holiday/clothes", "tags": {"all": 1, "woolen": 0, "scarf": 0, "clothes": 0}},
        {"name": "Winter Gloves", "link": "holiday/clothes", "tags": {"all": 1, "winter": 0, "gloves": 0, "clothes": 0}},
        {"name": "Holiday Cookies", "link": "holiday/food", "tags": {"all": 1, "holiday": 0, "cookies": 0, "food": 0}},
        {"name": "Chocolate Gift Box", "link": "holiday/food", "tags": {"all": 1, "chocolate": 0, "gift": 0, "box": 0, "food": 0}},
        {"name": "Gourmet Cheese Set", "link": "holiday/food", "tags": {"all": 1, "gourmet": 0, "cheese": 0, "set": 0, "food": 0}},
        {"name": "Scented Candle", "link": "holiday/scented", "tags": {"all": 1, "candle": 0, "scented": 0}},
        {"name": "Aromatic Diffuser", "link": "holiday/scented", "tags": {"all": 1, "aromatic": 0, "diffuser": 0, "scented": 0}},
        {"name": "Perfume Gift Set", "link": "holiday/scented", "tags": {"all": 1, "perfume": 0, "gift": 0, "set": 0, "scented": 0}}
    ]

# Save items to the JSON file
def save_items():
    with open(DATA_FILE, "w") as file:
        json.dump(items, file, indent=4)

# Initialize items
items = load_items()

@search_api.route('/search', methods=['GET', 'OPTIONS'])
def search_items():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    results = [
        item for item in items if query in item["name"].lower() or any(query in tag for tag in item["tags"])
    ]
    return jsonify(results)


@search_api.route('/increment_tag', methods=['POST', 'OPTIONS'])
def increment_tag():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({"message": "CORS preflight check passed!"})
        response.status_code = 200
        return response

    # Handle POST request
    data = request.get_json()
    item_name = data.get('name')
    item = next((item for item in items if item["name"].lower() == item_name.lower()), None)
    if item:
        for tag in item['tags']:
            item['tags'][tag] += 1
        save_items()  # Save updated tags to file
        return jsonify({"message": f"Tags for '{item_name}' updated successfully!", "tags": item["tags"]}), 200
    return jsonify({"error": "Item not found!"}), 404

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:4887')  # Match frontend origin
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Allow OPTIONS for preflight
    return response

# Register the Blueprint
app.register_blueprint(search_api)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8887)