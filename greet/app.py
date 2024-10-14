# app.py
import json


def handler(event, context):
    name = (event.get("queryStringParameters", None) or {}).get("name", "World")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Hello, {name}!"}),
        "headers": {"Content-Type": "application/json"},
    }
