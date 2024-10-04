from . import credit_score_rules_bp
from flask import request, jsonify
from dotenv import load_dotenv
from utils.config import S3
from helpers.error_helpers import handle_error
from helpers.s3_helpers.get_file_content import get_file_content_from_key
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from datetime import datetime
from ..credit_score_rules.rules_service import update_default_rules_logic
from helpers.auth_helpers import rules_api_key_required

# Fetch the API URL from the environment variables
S3_API_URL = S3["url"]
S3_FOLDER_NAME = S3["folder_name"]
RULES_SUBFOLDER_NAME = S3["rules_subfolder_name"]
DEFAULT_RULES_FILENAME = S3["default_rules_filename"]
LATEST_RULES_FILENAME = S3["latest_rules_filename"]

@credit_score_rules_bp.route('/fetch', methods=['GET'])
@rules_api_key_required
def get_credit_score_rules():
    rules_version = request.args.get('rules_version', default=None)

    try:
        # if no rules version specified, get defualt rules file
        if rules_version == None:
            default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)
            default_rules_file = default_rules_file_content["default_rules"]
            rules_version = default_rules_file

        rules_content = get_file_content_from_key(rules_version,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)

        return jsonify({"rules_file": rules_version,
                "rules":rules_content}), 200
    except Exception as e:
        return handle_error(f"Error getting rules: {str(e)}", 500)



# API to update the default rules file
@credit_score_rules_bp.route('/default-rules/update', methods=['POST'])
@rules_api_key_required
def update_default_rules():
    try:
        # Get the new rules file from the request
        new_default_rules_file = request.json.get('rules_file')
        updated_rules = update_default_rules_logic(new_default_rules_file)

        return jsonify({'message': 'Default rules file updated', 'new_default_rules_file': updated_rules}), 200

    except Exception as e:
        return handle_error(f"Error updating default rules: {str(e)}", 500)

# API to upload new rules
@credit_score_rules_bp.route('/upload', methods=['POST'])
@rules_api_key_required
def upload_rules():
    try:
        rules = request.json.get('rules')
        description = request.json.get('description','')
        set_default = request.json.get('set_default', False)
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        if not rules:
            return handle_error('Data for rules file is required', 400)

        # Prepare rules file content
        rules_content = {'timestamp': formatted_time,
                         'description':description,
                         'rules':rules}

        # Get latest rules version
        latest_version = get_file_content_from_key(LATEST_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)["latest_version"]

        # Increment version number for new filename
        current_version = latest_version + 1
        filename = f"rules_v{current_version}.json"

        # Upload new rules version file
        key = upload_file_to_s3(filename,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME,rules_content,True)
        latest_version_data = {"latest_version":current_version}

        if set_default:
            update_default_rules_logic(filename)  # Call the logic to update default rules

        # Upload latest version number for tracking
        upload_file_to_s3(LATEST_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME,latest_version_data,True)

        return jsonify({'message':'Rules file uploaded','key':key["key"]}), 201
    except Exception as e:
        return handle_error(f"Error uploading rules file: {str(e)}", 500)


# API to uploade new rules
@credit_score_rules_bp.route('/', methods=['GET'])
@rules_api_key_required
def get_rules():
    try:
        # Get latest rules version
        latest_version = get_file_content_from_key(LATEST_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)["latest_version"]
        rules_files = {}

        for version in range(1, latest_version + 1):
            rules = get_file_content_from_key( f"rules_v{version}.json", S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)
            # Check if the response is a dictionary and if it contains the expected data
            if not isinstance(rules, dict):
                    rules_files[f"rules_v{version}.json"] = "Something is wrong with this file. Unable to get file content."
            else:
                rules_files[f"rules_v{version}.json"] = rules

        return jsonify(rules_files), 200
    except Exception as e:
        return handle_error(f"Error getting rules files: {str(e)}", 500)