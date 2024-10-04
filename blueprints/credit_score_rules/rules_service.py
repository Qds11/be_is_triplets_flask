from helpers.s3_helpers.get_file_content import get_file_content_from_key
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from utils.config import S3

S3_FOLDER_NAME = S3["folder_name"]
RULES_SUBFOLDER_NAME = S3["rules_subfolder_name"]
DEFAULT_RULES_FILENAME = S3["default_rules_filename"]

def update_default_rules_logic(new_default_rules_file):
    if not new_default_rules_file:
        raise ValueError('New default rules file is required')

    data = {"default_rules": new_default_rules_file}
    upload_file_to_s3(DEFAULT_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME, data, True)
    default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME, S3_FOLDER_NAME, RULES_SUBFOLDER_NAME)

    return default_rules_file_content["default_rules"]

def get_default_rule():
    default_rules_file_content = get_file_content_from_key(DEFAULT_RULES_FILENAME,S3_FOLDER_NAME,RULES_SUBFOLDER_NAME)
    default_rules_file = default_rules_file_content["default_rules"]
    return default_rules_file