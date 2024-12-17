from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from google.cloud import pubsub_v1
import json
import threading


# Create a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/cloud-app-dev-yessimseit/topics/event-notifications'
# Create a subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_name = 'projects/cloud-app-dev-yessimseit/subscriptions/event-notifications-sub'



# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@34.56.82.40:5432/eventdatabase'
app.config['JWT_SECRET_KEY'] = 'pwd'  # Change this to a secure secret key

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Registration(db.Model):
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    ticket_type = db.Column(db.String(50))
    number_of_tickets = db.Column(db.Integer, nullable=False)

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    contact_info = db.Column(db.String(100))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class EventCategory(db.Model):
    __tablename__ = 'event_category'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# User registration route
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    # Hash the password before storing it
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        # Ensure the user ID is passed as a string for the 'sub' field in the token
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# Delete user route (protected by JWT)
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()  # This is now a string
    if current_user_id != str(user_id):  # Ensure user_id is a string for comparison
        return jsonify({"message": "Unauthorized to delete this user."}), 403
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


# Create event route (protected by JWT)
@app.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    data = request.json
    created_by = get_jwt_identity()  # Get the user ID from the JWT token
    
    new_event = Event(
        title=data['title'],
        description=data.get('description', ''),
        date_time=datetime.strptime(data['date_time'], "%Y-%m-%d %H:%M:%S"),
        location=data.get('location', ''),
        created_by=created_by
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created successfully!"}), 201

def publish_payment_message(payment_id):
    message = {
        'payment_id': payment_id,
        'status': 'pending'
    }
    # Publish message to Pub/Sub
    publisher.publish(topic_name, json.dumps(message).encode('utf-8'))


def run_subscriber():
    listen_for_payment_notifications()
        

# Subscribe to the Pub/Sub topic
def listen_for_payment_notifications():
    subscriber.subscribe(subscription_name, callback=callback)

# Register for event route (protected by JWT)
@app.route('/register_event', methods=['POST'])
@jwt_required()
def register_for_event():
    data = request.json
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    
    # Create registration
    registration = Registration(
        user_id=user_id,
        event_id=data['event_id'],
        ticket_type=data['ticket_type'],
        number_of_tickets=data['number_of_tickets']
    )
    db.session.add(registration)
    db.session.commit()

    # Create payment record with status 'pending'
    payment = Payment(
        registration_id=registration.id,
        amount=data['amount'],
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()

    # Publish payment message to Pub/Sub
    publish_payment_message(payment.id)

    return jsonify({"message": "Registration successful!"}), 201

# Create category route (protected by JWT)
@app.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.json
    new_category = Category(
        name=data['name'],
        description=data['description']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully!"}), 201

# Get all events route (can be public or protected)
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{'id': event.id, 'title': event.title, 'description': event.description} for event in events]
    return jsonify(events_list)

# Get all categories route (can be public or protected)
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [{'id': category.id, 'name': category.name, 'description': category.description} for category in categories]
    return jsonify(categories_list)

def callback(message):
    # Parse the incoming message
    message_data = json.loads(message.data.decode('utf-8'))
    
    payment_id = message_data['payment_id']
    status = message_data['status']
    
    # Update payment status in the database
    payment = Payment.query.get(payment_id)
    if payment:
        payment.status = status
        db.session.commit()

        # Create notification about successful payment
        notification = Notification(
            user_id=payment.registration.user_id,
            event_id=payment.registration.event_id,
            message=f"Payment for event {payment.registration.event_id} has been successfully completed.",
        )
        db.session.add(notification)
        db.session.commit()

        # Acknowledge the message
        message.ack()


def publish_payment_message(payment_id):
    message = {
        'payment_id': payment_id,
        'status': 'pending'
    }
    # Publish message to Pub/Sub
    publisher.publish(topic_name, json.dumps(message).encode('utf-8'))

# Run the subscriber in a separate thread
def run_subscriber():
    listen_for_payment_notifications()

# # Create tables
# with app.app_context():
#     db.create_all()
import threading

\

if __name__ == '__main__':
    # Start the subscriber thread
    subscriber_thread = threading.Thread(target=run_subscriber)
    subscriber_thread.start()
    
    # Run the Flask app
    app.run(debug=True)