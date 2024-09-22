from . import credit_score_rules_bp
from flask import request, jsonify
from dotenv import load_dotenv
from utils.config import S3
from helpers.error_helpers import handle_error
from helpers.s3_helpers.get_file_content import get_file_content_from_key
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3

# Load environment variables from .env.development
load_dotenv('.env.development')

# Fetch the API URL from the environment variables
S3_API_URL = S3["url"]
S3_FOLDER_NAME = S3["folder_name"]
RULES_SUBFOLDER_NAME = S3["rules_subfolder_name"]
DEFAULT_RULES_FILENAME = S3["default_rules_filename"]

@credit_score_rules_bp.route('/fetch', methods=['GET'])
def get_credit_score_rules():
    default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)
    default_rules_file = default_rules_file_content["default_rules"]
    default_rules = get_file_content_from_key(default_rules_file,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)
    return {"default_rules_file": default_rules_file,
            "default_rules":default_rules}


# API to update the default rules file
@credit_score_rules_bp.route('/update', methods=['POST'])
def update_default_rules():
    try:
        # Get the new rules file from the request
        new_default_rules_file = request.json.get('rules_file')

        if not new_default_rules_file:
            return handle_error('New rules file is required', 400)

        data = {"default_rules":new_default_rules_file}
        upload_file_to_s3(DEFAULT_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME,data,True)
        default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)

        return jsonify({'message': 'Default rules file updated', 'new_default_rules_file': default_rules_file_content["default_rules"]}), 200

    except Exception as e:
        return handle_error(f"Error updating default rules: {str(e)}", 500)
