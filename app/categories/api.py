from flask import request, jsonify, Blueprint
from app import db
from app.categories.schemas import *
from app.models import Category
from app.validate_json import validate_json

categories = Blueprint('categories', '__name__')


@categories.route('/category', methods=['POST'])
@validate_json(add_category_schema)
def add_category():
    category = Category.query.filter_by(name=request.json['name']).first()
    if category:
        return jsonify({"Error": 'Category Already exists'}), 404
    new_category = Category(name=request.json['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"Action": 'Category created'}), 201


@categories.route('/category')
def get_categories():
    category = Category.query.all()
    if not category:
        return jsonify({"Error": 'No categories found'}), 404

    return jsonify(category), 200


@categories.route('/category/<int:category_id>')
def get_category(category_id):
    category = Category.query.get(category_id)
    if category:
        return jsonify(category), 200

    return jsonify({"Error": 'No category found'}), 404


@categories.route('/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"Error": 'No category found'}), 404
    category.name = request.json['name']
    return jsonify({"Action": 'Category updated'}), 201


@categories.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"Error": 'No category found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"Action": 'Category deleted'}), 201
