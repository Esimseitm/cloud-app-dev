from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Category
from app.extensions import db

category_bp = Blueprint('categories', __name__)

@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.json
    new_category = Category(name=data['name'], description=data['description'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully!"}), 201

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in categories])
