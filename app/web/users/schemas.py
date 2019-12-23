add_user_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 5},
        "username": {"type": "string", "minLength": 2},
        "password": {"type": "string", "minLength": 8},
    },
    "required": ["email", "username", "password", "confirm_password"]
}

login_user_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 5},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
}

change_password_schema = {
    "type": "object",
    "properties": {
        "old_password": {"type": "string", "minLength": 8},
        "new_password": {"type": "string", "minLength": 8},
        "confirm_password": {"type": "string", "minLength": 8},

    },
    "required": ["old_password", "new_password", "confirm_password"]
}

