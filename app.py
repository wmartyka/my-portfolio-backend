from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import pytz
import os

app = Flask(__name__)
CORS(app)

# Database configuration for Render (PostgreSQL preferred, fallback to SQLite for local testing)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///submissions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set the local timezone to Austin, TX (Central Time)
local_timezone = pytz.timezone('America/Chicago')

# Define database model for storing submissions
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)  # Store in UTC

    def local_time(self):
        """Convert UTC time to Austin (Central Time)"""
        return self.submitted_at.replace(tzinfo=pytz.utc).astimezone(local_timezone)

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

        if not name or not email:
            return jsonify({'error': 'All fields are required'}), 400

        # Save submission to database with UTC time
        new_submission = Submission(name=name, email=email)
        db.session.add(new_submission)
        db.session.commit()

        return jsonify({'message': f'Thank you {name}, we will contact you at {email}.'}), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/submissions', methods=['GET'])
def get_submissions():
    submissions = Submission.query.order_by(Submission.submitted_at.desc()).all()
    submissions_data = [
        {
            "id": sub.id,
            "name": sub.name,
            "email": sub.email,
            "submitted_at": sub.local_time().strftime("%B %d, %Y %I:%M %p")  # Convert to CST/CDT with AM/PM
        }
        for sub in submissions
    ]
    return jsonify(submissions_data)

if __name__ == '__main__':
    app.run(debug=True)
