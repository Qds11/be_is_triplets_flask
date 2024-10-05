from . import source_data_bp
from flask import request, jsonify
from helpers.auth_helpers import credit_evaluation_api_key_required
from helpers.error_helpers import handle_error
from .source_data_service import ocr_method

@source_data_bp.route('/', methods=['POST'])
@credit_evaluation_api_key_required
def get_source_data():
    try:
        request_data = request.json
        urls = request_data.get('urls', None)

        if not urls or not isinstance(urls, list):
            return handle_error('A list of document URLs is required', 400)

        source_data = ocr_method(urls)

        return jsonify(source_data), 201


    except Exception as e:
        print(f"Error getting source data: {str(e)}")
        return jsonify({'error': f"Error getting source data: {str(e)}"}), 500