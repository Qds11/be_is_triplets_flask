from . import credit_score_bp
from flask import request, request, jsonify
from utils.config import S3
 # Import helper functions
from helpers.api_helpers import get_source_data, get_financial_ratio, get_rules
from helpers.error_helpers import handle_error
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from helpers.auth_helpers import api_key_required

S3_FOLDER_NAME = S3["folder_name"]
RESULTS_SUBFOLDER_NAME = S3["results_subfolder_name"]


@credit_score_bp.route('/', methods=['POST'])
@api_key_required
def get_credit_score():
    try:
        request_data = request.json
        urls  = request_data.get('urls', None)

        if not urls or len(urls)==0:
            return handle_error('A list of document URLs is required', 400)

        # Call the helper functions
        source_data = get_source_data(urls )
        financial_ratio = get_financial_ratio(source_data)
        rules_file = get_rules()
        rules_file_name = rules_file["default_rules_file"]
        rules_file_content = rules_file["default_rules"]

        result = {
            'financial_ratio': financial_ratio,
            'rules_file': rules_file_name
        }
        response_data = upload_file_to_s3("test.json",S3_FOLDER_NAME, RESULTS_SUBFOLDER_NAME, result )

        return jsonify(response_data), 200

    except Exception as e:
        return handle_error(f"Error getting credit score: {str(e)}", 500)

