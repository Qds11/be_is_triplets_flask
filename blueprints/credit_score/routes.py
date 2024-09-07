from . import credit_score_bp
from flask import request, request, jsonify, url_for
from dotenv import load_dotenv
import requests
import json
import os
from utils.config import S3_API_HEADERS

# Load environment variables from .env.development
load_dotenv('.env.development')

# Fetch the API URL from the environment variables
S3_API_URL = os.getenv('S3_API_URL')
S3_FOLDER_NAME = os.getenv('S3_FOLDER_NAME')
RULES_SUBFOLDER_NAME = os.getenv('RULES_SUBFOLDER_NAME')

@credit_score_bp.route('/', methods=['POST'])
def get_credit_score():
    try:
        request_data = request.json
        document_url = request_data.get('url', None)
        rules_file = request_data.get('rules', "e0eceef8136ecfaadca1aa40b2b84e2b.json")

        if not document_url:
            return jsonify({'error': 'Document url(s) is required'}), 400

        source_data = get_source_data(document_url)

        financial_ratio = get_financial_ratio(source_data)
        rules = get_rules(rules_file)

        result = rules
        return result
    except Exception as e:
        print(f"Error getting source data: {str(e)}")
        return jsonify({'error': f"Error getting source data: {str(e)}"}), 500


def get_source_data(document_url):
    source_data_url = url_for('source_data.get_source_data', _external=True)

    # Make a POST request to the source_data route with the document_id
    response = requests.post(source_data_url, json={'url': document_url})
    if response.status_code == 200:
        source_data = response.json()
        # You can now work with source_data to calculate the financial ratio
        return source_data
    else:
        return jsonify({'error': 'Could not retrieve source data'}), response.status_code

def get_financial_ratio(source_data):
    financial_ratio_url = url_for('financial_ratio.get_financial_ratio', _external=True)
    # Make a POST request to the source_data route with the document_id
    response = requests.post(financial_ratio_url, json={'source_data': source_data})
    if response.status_code == 200:
        financial_ratio = response.json()
        # You can now work with source_data to calculate the financial ratio
        return financial_ratio
    else:
        return jsonify({'error': 'Could not retrieve source data'}), response.status_code

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
            print(response_data)
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