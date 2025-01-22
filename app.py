from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/')
def home():
    return jsonify({"message": "Backend is running successfully!"})

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        
        # Extract form data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()

        # Validate input fields
        if not name or not email:
            return jsonify({'error': 'All fields are required'}), 400

        # Success response
        return jsonify({'message': f'Python Thanks you {name}, we will contact you at {email}.'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
