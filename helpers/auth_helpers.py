from flask import request, jsonify
from functools import wraps
from utils.config import CREDIT_EVALUATION_API_KEY, RULES_API_KEY  # Import the API key from the config

def credit_evaluation_api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the X-Contacts-Key header is present
        api_key = request.headers.get('X-Contacts-Key')

        if not api_key:
            return jsonify({"error": "API key is missing"}), 401

        # Validate the API key from the config
        if api_key != CREDIT_EVALUATION_API_KEY:
            return jsonify({"error": "Unauthorized. Invalid API key"}), 401

        return f(*args, **kwargs)
    return decorated_function

def rules_api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the X-Contacts-Key header is present
        api_key = request.headers.get('X-Contacts-Key')

        if not api_key:
            return jsonify({"error": "API key is missing"}), 401
        # Validate the API key from the config
        if api_key != RULES_API_KEY:
            return jsonify({"error": "Unauthorized. Invalid API key"}), 401

        return f(*args, **kwargs)
    return decorated_function
