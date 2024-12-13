from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@34.56.82.40:5432/eventdb'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)