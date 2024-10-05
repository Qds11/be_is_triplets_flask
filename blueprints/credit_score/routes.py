from . import credit_score_bp
from flask import request, request, jsonify
from utils.config import S3
 # Import helper functions
from helpers.service_helpers import get_source_data, get_financial_ratio, get_rules
from helpers.error_helpers import handle_error
from helpers.s3_helpers.upload_file_helper import upload_file_to_s3
from helpers.auth_helpers import credit_evaluation_api_key_required
from .credit_score_service import calculate_credit_score, get_credit_grade
S3_FOLDER_NAME = S3["folder_name"]
RESULTS_SUBFOLDER_NAME = S3["results_subfolder_name"]

@credit_score_bp.route('/', methods=['POST'])
@credit_evaluation_api_key_required
def get_credit_score():
    try:
        request_data = request.json
        urls  = request_data.get('urls', None)
        rules_version  = request_data.get('rules_version', None)

        if not urls or len(urls)==0:
            return handle_error('A list of document URLs is required', 400)

        # Call the api helper functions to call modules
        source_data = get_source_data(urls ) # Call source data module to retrieve raw data from financial statements
        financial_ratio = get_financial_ratio(source_data)  # Call financial ratio module to get return financial ratios

        rules_file_name = None

        if rules_version:
            rules_file_name =f"rules_v{rules_version}.json"

        rules_file_content = get_rules(rules_file_name) # Call rules module to get rules needed to calculate the credit rating
        rules_file_name = rules_file_content["rules_file"]
        rules_file_content = rules_file_content["rules"]["rules"]

        credit_score = calculate_credit_score(rules_file_content,financial_ratio)

        risk_grade = get_credit_grade(credit_score)


        result = {
            'financial_ratio': financial_ratio,
            'rules_file_name':rules_file_name,
            'rules':rules_file_content,
            'credit_score': credit_score,
            'risk_grade': risk_grade,
            'extracted_data':source_data
        }

        print(result)

        response_data = upload_file_to_s3("test.json",S3_FOLDER_NAME, RESULTS_SUBFOLDER_NAME, result )

        return jsonify(response_data), 200

    except Exception as e:
        return handle_error(f"Error getting credit score: {str(e)}", 500)

