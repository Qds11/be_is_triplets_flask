from . import credit_score_rules_bp
from flask import request, jsonify
from dotenv import load_dotenv
import requests
import json
from utils.config import S3, DEFAULT_RULES
from helpers.s3_helpers.fetch_file_helper import fetch_file_url_from_s3
from helpers.error_helpers import handle_error

# Load environment variables from .env.development
load_dotenv('.env.development')

# Fetch the API URL from the environment variables
S3_API_URL = S3["url"]
S3_FOLDER_NAME = S3["folder_name"]
RULES_SUBFOLDER_NAME = S3["rules_subfolder_name"]

@credit_score_rules_bp.route('/fetch', methods=['POST'])
def get_credit_score_rules():
    try:
        # Extracting the rules_file from the request payload, or using DEFAULT_RULES
        request_data = request.json
        rules_file = request_data.get('rules_file', DEFAULT_RULES)

        # Check for missing parameters
        if not rules_file:
            return handle_error('Missing required rules filename', 400)

        response_data = fetch_file_url_from_s3(rules_file, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)

        file_url = response_data.get('url')

        if not file_url:
            return handle_error('File URL not found in the response', 500)

        # Fetch the file content using the URL
        file_response = requests.get(file_url)
        if file_response.status_code != 200:
            return handle_error(f"Unable to download the file from {file_url}. Status code: {file_response.status_code}", 500)

        # Parse the file content as JSON
        try:
            file_content = json.loads(file_response.text)
            return jsonify(file_content), 200
        except json.JSONDecodeError as e:
            return handle_error(f"Failed to parse JSON from the file. Error: {str(e)}", 500)

    except requests.exceptions.RequestException as re:
        # Capture specific request-related errors
        return handle_error(f"Network error occurred: {str(re)}", 500)

    except Exception as e:
        # Capture all other errors
        return handle_error(f"An unexpected error occurred: {str(e)}", 500)


# API to update the default rules file
@credit_score_rules_bp.route('/update', methods=['POST'])
def update_default_rules():
    global DEFAULT_RULES
    try:
        # Get the new rules file from the request
        new_rules_file = request.json.get('rules_file')

        if not new_rules_file:
            return handle_error('New rules file is required', 400)

        # Update the global DEFAULT_RULES
        DEFAULT_RULES = new_rules_file

        return jsonify({'message': 'Default rules file updated', 'new_default_rules': DEFAULT_RULES}), 200

    except Exception as e:
        return handle_error(f"Error updating default rules: {str(e)}", 500)
