from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend origin (GitHub Pages URL)
CORS(app, resources={r"/*": {"origins": "https://wmartyka.github.io"}})

# Home route to check if backend is running
@app.route('/')
def home():
    return jsonify({"message": "Backend is running successfully!"})

# Handle form submission with POST method
@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit_form():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    try:
        data = request.get_json()

        # Validate input fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({'error': 'All fields are required'}), 400

        return jsonify({'message': f'Thank you {name}, we will contact you at {email}.'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
