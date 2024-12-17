from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Event
from app.extensions import db
from datetime import datetime

event_bp = Blueprint('events', __name__)

@event_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    data = request.json
    created_by = get_jwt_identity()
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

@event_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{'id': e.id, 'title': e.title, 'description': e.description} for e in events]
    return jsonify(events_list)
