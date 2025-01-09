from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with appropriate settings
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:4887"], methods=["GET", "POST", "OPTIONS"])

# Define the Blueprint
search_api = Blueprint('search_api', __name__)

# Sample items with a count for each tag
items = [
    {"name": "Teddy Bear", "link": "holiday/toys", "tags": {"all": 0, "teddy": 0, "bear": 0, "toys": 0}},
    {"name": "Lego Set", "link": "holiday/toys", "tags": {"all": 0, "lego": 0, "set": 0, "toys": 0}},
    {"name": "Remote Control Car", "link": "holiday/toys", "tags": {"all": 0, "remote": 0, "control": 0, "car": 0, "toys": 0}},
    {"name": "Holiday Candles", "link": "holiday/home-decor", "tags": {"all": 0, "holiday": 0, "candles": 0, "home-decor": 0}},
    {"name": "Festive Wreath", "link": "holiday/home-decor", "tags": {"all": 0, "festive": 0, "wreath": 0, "home-decor": 0}},
    {"name": "Decorative Ornaments", "link": "holiday/home-decor", "tags": {"all": 0, "decorative": 0, "ornaments": 0, "home-decor": 0}},
    {"name": "Wireless Headphones", "link": "holiday/electronics", "tags": {"all": 0, "wireless": 0, "headphones": 0, "electronics": 0}},
    {"name": "Smartwatch", "link": "holiday/electronics", "tags": {"all": 0, "smartwatch": 0, "electronics": 0}},
    {"name": "Gaming Console", "link": "holiday/electronics", "tags": {"all": 0, "gaming": 0, "console": 0, "electronics": 0}},
    {"name": "Cozy Holiday Sweater", "link": "holiday/clothes", "tags": {"all": 0, "cozy": 0, "holiday": 0, "sweater": 0, "clothes": 0}},
    {"name": "Woolen Scarf", "link": "holiday/clothes", "tags": {"all": 0, "woolen": 0, "scarf": 0, "clothes": 0}},
    {"name": "Winter Gloves", "link": "holiday/clothes", "tags": {"all": 0, "winter": 0, "gloves": 0, "clothes": 0}},
    {"name": "Holiday Cookies", "link": "holiday/food", "tags": {"all": 0, "holiday": 0, "cookies": 0, "food": 0}},
    {"name": "Chocolate Gift Box", "link": "holiday/food", "tags": {"all": 0, "chocolate": 0, "gift": 0, "box": 0, "food": 0}},
    {"name": "Gourmet Cheese Set", "link": "holiday/food", "tags": {"all": 0, "gourmet": 0, "cheese": 0, "set": 0, "food": 0}},
    {"name": "Scented Candle", "link": "holiday/scented", "tags": {"all": 0, "candle": 0, "scented": 0}},
    {"name": "Aromatic Diffuser", "link": "holiday/scented", "tags": {"all": 0, "aromatic": 0, "diffuser": 0, "scented": 0}},
    {"name": "Perfume Gift Set", "link": "holiday/scented", "tags": {"all": 0, "perfume": 0, "gift": 0, "set": 0, "scented": 0}}
]

@search_api.route('/search', methods=['GET', 'OPTIONS'])
def search_items():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({"message": "CORS preflight check passed!"})
        response.status_code = 200
        return response
    
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])  # Return an empty list if no query is provided
    results = [item for item in items if query in item["name"].lower()]
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
        # Increment all tag counts for the selected item
        for tag in item['tags']:
            item['tags'][tag] += 1
        return jsonify({"message": f"Tags for '{item_name}' updated successfully!", "tags": item["tags"]}), 200
    return jsonify({"error": "Item not found!"}), 404

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:4887')  # Match your frontend origin
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

# Register the Blueprint
app.register_blueprint(search_api)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8887)
