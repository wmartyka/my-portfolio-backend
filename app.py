from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my portfolio backend!"

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Missing data'}), 400
    return jsonify({'message': f'Thank you, {name}! We will contact you at {email}.'})

if __name__ == '__main__':
    app.run(debug=True)
