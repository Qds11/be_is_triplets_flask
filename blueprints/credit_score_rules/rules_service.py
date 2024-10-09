from helpers.s3_helpers.get_file_content import get_file_content_from_key
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from utils.config import S3
from datetime import datetime

S3_FOLDER_NAME = S3["folder_name"]
RULES_SUBFOLDER_NAME = S3["rules_subfolder_name"]
DEFAULT_RULES_FILENAME = S3["default_rules_filename"]
LATEST_RULES_FILENAME = S3["latest_rules_filename"]

# Logic to update the default rules
def update_default_rules(new_default_rules_file):
    if not new_default_rules_file:
        raise ValueError('New default rules file is required')

    data = {"default_rules": new_default_rules_file}
    upload_file_to_s3(DEFAULT_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME, data, True)
    default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)

    return default_rules_file_content["default_rules"]

# Logic to get the default rule
def get_default_rule():
    default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)
    default_rules_file = default_rules_file_content["default_rules"]
    return default_rules_file

# Logic to fetch the rules (by version or default)
def fetch_rules(rules_version=None):
    if not rules_version:
        rules_version = get_default_rule()
    rules_file = f"rules_v{rules_version}.json"
    rules_content = get_file_content_from_key(rules_file, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)
    return {"rules_file": rules_file, "rules": rules_content}

# Logic to upload new rules
def upload_rules_service(rules, description='', set_default=False):
    try:
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Prepare rules file content
        rules_content = {
            'timestamp': formatted_time,
            'description': description,
            'rules': rules
        }

        # Get latest rules version
        latest_version = get_file_content_from_key(LATEST_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)["latest_version"]
        current_version = latest_version + 1
        filename = f"rules_v{current_version}.json"

        # Upload new rules version file
        key = upload_file_to_s3(filename, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME, rules_content, True)
        latest_version_data = {"latest_version": current_version}

        if set_default:
            update_default_rules(filename)  # Call the logic to update default rules

        # Upload latest version number for tracking
        upload_file_to_s3(LATEST_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME, latest_version_data, True)

        return {'message': 'Rules file uploaded', 'key': key["key"]}

    except Exception as e:
        raise Exception(f"Error uploading rules file: {str(e)}")

# Logic to get all rules
def get_all_rules():
    try:
        latest_version = get_file_content_from_key(LATEST_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)["latest_version"]
        rules_files = {}

        for version in range(1, latest_version + 1):
            rules = get_file_content_from_key(f"rules_v{version}.json", S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)
            if not isinstance(rules, dict):
                rules_files[f"rules_v{version}.json"] = "Something is wrong with this file. Unable to get file content."
            else:
                rules_files[f"rules_v{version}.json"] = rules

        return rules_files
    except Exception as e:
        raise Exception(f"Error getting rules files: {str(e)}")
