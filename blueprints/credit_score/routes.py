from . import credit_score_bp
from flask import request, request, jsonify, url_for
from utils.config import DEFAULT_RULES, S3
 # Import helper functions
from helpers.api_helpers import get_source_data, get_financial_ratio, get_rules
from helpers.error_helpers import handle_error
from helpers.upload_file_helper import upload_file_to_s3

S3_FOLDER_NAME = S3["folder_name"]

@credit_score_bp.route('/', methods=['POST'])
def get_credit_score():
    try:
        request_data = request.json
        document_url = request_data.get('url', None)
        rules_file = request_data.get('rules_file', DEFAULT_RULES)

        if not document_url:
            return handle_error('Document URL is required', 400)

        # Call the helper functions
        source_data = get_source_data(document_url)
        financial_ratio = get_financial_ratio(source_data)
        rules = get_rules(rules_file)

        result = {
            'financial_ratio': financial_ratio,
            'rules_file': rules_file
        }
        response_data = upload_file_to_s3("test.json",S3_FOLDER_NAME, "Results", result )

        return jsonify(response_data), 200

    except Exception as e:
        return handle_error(f"Error getting credit score: {str(e)}", 500)

