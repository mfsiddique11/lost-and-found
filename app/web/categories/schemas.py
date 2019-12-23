add_category_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}
    },
    "required": ["name"]
}


update_category_schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "itemName": {"type": "string", "minLength": 2},
        "location": {"type": "string", "minLength": 2}
    }
}
