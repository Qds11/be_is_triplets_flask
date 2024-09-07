from flask import jsonify

# Centralized function for error handling
def handle_error(message, status_code=500):
    response = jsonify({'error': message})
    response.status_code = status_code
    return response
