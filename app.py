from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes and allow only your frontend origin
CORS(app, resources={r"/*": {"origins": "https://wmartyka.github.io"}})

@app.route('/')
def home():
    return "Welcome to my portfolio backend!"

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'All fields are required'}), 400

    return jsonify({'message': f'Thank you {name}, we will contact you at {email}.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
