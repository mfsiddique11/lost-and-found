from flask import jsonify, request, Response
from functools import wraps
from jsonschema import validate, ValidationError


def validate_json(schema):
    def json_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            form_data = request.form

            if data:
                # return Response(status=400)
                try:
                    validate(data, schema=schema)
                except ValidationError as e:
                    return jsonify({"Error": e.message}), 400
            else:
                try:
                    validate(form_data, schema=schema)
                except ValidationError as e:
                    return jsonify({"Error": e.message}), 400

            return func(*args, **kwargs)

        return decorated_function

    return json_decorator
