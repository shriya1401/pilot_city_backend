from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    return jsonify({"message": "Data received successfully", "receivedData": data})

if __name__ == '__main__':
    app.run(debug=True)
