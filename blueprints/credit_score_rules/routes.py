from . import credit_score_rules_bp
from flask import request, request, jsonify, url_for
from dotenv import load_dotenv
import requests
import json
import os
from utils.config import S3_API_HEADERS, DEFAULT_RULES

# Load environment variables from .env.development
load_dotenv('.env.development')

# Fetch the API URL from the environment variables
S3_API_URL = os.getenv('S3_API_URL')
S3_FOLDER_NAME = os.getenv('S3_FOLDER_NAME')
RULES_SUBFOLDER_NAME = os.getenv('RULES_SUBFOLDER_NAME')

@credit_score_rules_bp.route('/fetch', methods=['POST'])
def get_credit_score_rules():
    try:
        request_data = request.json
        rules_file = request_data.get('rules_file', DEFAULT_RULES)

        rules = get_rules(rules_file)

        return rules
    except Exception as e:
        print(f"Error getting rules: {str(e)}")
        return jsonify({'error': f"Error getting rules: {str(e)}"}), 500


def get_rules(rules_file):
    fetch_url = S3_API_URL + "/FetchFileUrl"
    # Check for missing parameters
    if not rules_file:
        return jsonify({'error': 'Error when getting rules. Missing required rules filename'}), 400

    # Prepare the payload for the external API
    payload = {
        "folderName": S3_FOLDER_NAME,
        "subFolderName": RULES_SUBFOLDER_NAME,
        "key": rules_file
    }

    try:
        # Send POST request to the external API
        response = requests.post(fetch_url, json=payload, headers=S3_API_HEADERS)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response to get the file URL
            response_data = response.json()
            file_url = response_data.get('url')

            if not file_url:
                return jsonify({'error': 'File URL not found in the response'}), 500

            # Fetch the file content using the URL (optional)
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                try:
                    # Parse the file content as JSON
                    file_content = json.loads(file_response.text)

                    return jsonify(file_content), 200  # Return parsed JSON directly
                except json.JSONDecodeError as e:
                    return jsonify({"error": f"Failed to parse JSON from the file: {str(e)}"}), 500
            else:
                return jsonify({"error": f"Unable to download the file from {file_url}"}), 500

        else:
            return jsonify({'error': f"Failed to fetch file URL. Status code: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


# API to update the default rules file
@credit_score_rules_bp.route('/update', methods=['POST'])
def update_default_rules():
    global DEFAULT_RULES  # Modify the global default rules
    try:
        # Get the new rules file from the request
        new_rules_file = request.json.get('rules_file')

        if not new_rules_file:
            return jsonify({'error': 'New rules file is required'}), 400

        # Update the global DEFAULT_RULES
        DEFAULT_RULES = new_rules_file

        return jsonify({'message': 'Default rules file updated', 'new_default_rules': DEFAULT_RULES}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500