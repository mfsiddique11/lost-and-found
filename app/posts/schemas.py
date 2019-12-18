add_post_schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "itemName": {"type": "string", "minLength": 2},
        "location": {"type": "string", "minLength": 2}
    },
    "required": ["category", "description", "itemName", "location", "image"]
}


update_post_schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "itemName": {"type": "string", "minLength": 2},
        "location": {"type": "string", "minLength": 2}
    }
}
