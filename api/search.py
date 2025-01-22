import os
import sys

# Dynamically add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from model.search import SearchHistory, db

# Initialize Flask app
app = Flask(__name__)

# Apply CORS settings to the app
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:4887"])

# Define the Blueprint
search_api = Blueprint("search_api", __name__, url_prefix="/api/search")

# Items data
items = [
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

@search_api.route("/api/search", methods=["GET", "OPTIONS"])
def search_items():
    if request.method == "OPTIONS":
        return _cors_preflight_response()

    query = request.args.get("q", "").lower()
    user_id = request.args.get("user_id", "guest")  # Simulate user identification (default to "guest")

    if not query:
        return jsonify([])

    # Search logic
    results = [
        item for item in items if query in item["name"].lower() or any(query in tag for tag in item["tags"])
    ]

    # Save search query to the database
    try:
        associated_tags = [item["tags"] for item in results]
        search_entry = SearchHistory(user=user_id, query=query, tags=associated_tags)
        db.session.add(search_entry)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to log search query: {str(e)}"}), 500

    return jsonify(results), 200


@search_api.route("/increment_tag", methods=["POST", "OPTIONS"])
def increment_tag():
    if request.method == "OPTIONS":
        return _cors_preflight_response()

    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid data"}), 400

    item_name = data["name"]
    item = next((item for item in items if item["name"].lower() == item_name.lower()), None)
    if item:
        for tag in item["tags"]:
            item["tags"][tag] += 1
        return jsonify({"message": f"Tags for '{item_name}' updated successfully!", "tags": item["tags"]}), 200

    return jsonify({"error": "Item not found!"}), 404


def _cors_preflight_response():
    """
    Helper function to return a 200 OK response for CORS preflight requests.
    """
    response = jsonify({"message": "CORS preflight check passed!"})
    response.status_code = 200
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4887")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

@app.after_request
def add_cors_headers(response):
    """
    Ensures all responses include the necessary CORS headers.
    """
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4887")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response


# Register the Blueprint
app.register_blueprint(search_api)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8887)
