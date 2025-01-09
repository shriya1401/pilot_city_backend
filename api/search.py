from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Define the Blueprint
search_api = Blueprint('search_api', __name__)

# Sample items
items = [
    {"name": "Teddy Bear", "link": "holiday/toys", "tags": ["all", "teddy", "bear", "toys"]},
    {"name": "Lego Set", "link": "holiday/toys", "tags": ["all", "lego", "set", "toys"]},
    {"name": "Remote Control Car", "link": "holiday/toys", "tags": ["all", "remote", "control", "car", "toys"]},
    {"name": "Holiday Candles", "link": "holiday/home-decor", "tags": ["all", "holiday", "candles", "home-decor"]},
    {"name": "Festive Wreath", "link": "holiday/home-decor", "tags": ["all", "festive", "wreath", "home-decor"]},
    {"name": "Decorative Ornaments", "link": "holiday/home-decor", "tags": ["all", "decorative", "ornaments", "home-decor"]},
    {"name": "Wireless Headphones", "link": "holiday/electronics", "tags": ["all", "wireless", "headphones", "electronics"]},
    {"name": "Smartwatch", "link": "holiday/electronics", "tags": ["all", "smartwatch", "electronics"]},
    {"name": "Gaming Console", "link": "holiday/electronics", "tags": ["all", "gaming", "console", "electronics"]},
    {"name": "Cozy Holiday Sweater", "link": "holiday/clothes", "tags": ["all", "cozy", "holiday", "sweater", "clothes"]},
    {"name": "Woolen Scarf", "link": "holiday/clothes", "tags": ["all", "woolen", "scarf", "clothes"]},
    {"name": "Winter Gloves", "link": "holiday/clothes", "tags": ["all", "winter", "gloves", "clothes"]},
    {"name": "Holiday Cookies", "link": "holiday/food", "tags": ["all", "holiday", "cookies", "food"]},
    {"name": "Chocolate Gift Box", "link": "holiday/food", "tags": ["all", "chocolate", "gift", "box", "food"]},
    {"name": "Gourmet Cheese Set", "link": "holiday/food", "tags": ["all", "gourmet", "cheese", "set", "food"]},
    {"name": "Scented Candle", "link": "holiday/scented", "tags": ["all", "candle", "scented"]},
    {"name": "Aromatic Diffuser", "link": "holiday/scented", "tags": ["all", "aromatic", "diffuser", "scented"]},
    {"name": "Perfume Gift Set", "link": "holiday/scented", "tags": ["all", "perfume", "gift", "set", "scented"]}
]

# Define the /search route
@search_api.route('/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])  # Return an empty list if no query is provided
    results = [item for item in items if query in item["name"].lower()]
    return jsonify(results)

# A mock route to handle get credentials request
@app.route('/api/id', methods=['GET'])
def get_item_id():
    return jsonify({"message": "API running!"})

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Backend is working!"})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8887)