from flask import jsonify
from functools import wraps

from app.models.category_model import Category


def category_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        category = Category.query.all()
        if not category:
            return jsonify({"Error": "categories are not added"}), 400
        return func(*args, **kwargs)
    return decorated_function
