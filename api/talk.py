from flask import Flask, request, jsonify, Blueprint

app = Flask(__name__)
talk_api = Blueprint('talk_api', __name__)

@app.route('/socialmedia_frontend/talk.js', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    return jsonify({"message": "Data received successfully", "receivedData": data})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8209)
