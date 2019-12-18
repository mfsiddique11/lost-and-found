from flask import jsonify, request, Response
from app.models import Category
from functools import wraps


def category_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        category = Category.query.all()
        if not category:
            return jsonify({"Error": "categories are not added"}), 400
        return func(*args, **kwargs)
    return decorated_function
