from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration (Using SQLite or Render PostgreSQL)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///submissions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define database model
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Backend is running successfully!"})

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()

        # Validate input fields
        if not name or not email:
            return jsonify({'error': 'All fields are required'}), 400

        # Save submission to the database
        new_submission = Submission(name=name, email=email)
        db.session.add(new_submission)
        db.session.commit()

        return jsonify({'message': f'Thank you {name}, we will contact you at {email}.'}), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/submissions', methods=['GET'])
def get_submissions():
    submissions = Submission.query.all()
    submissions_data = [{"id": sub.id, "name": sub.name, "email": sub.email} for sub in submissions]
    return jsonify(submissions_data)

if __name__ == '__main__':
    app.run(debug=True)
