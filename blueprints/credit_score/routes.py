from . import credit_score_bp
from flask import request, request, jsonify, url_for
from dotenv import load_dotenv
import requests
import json
import os
from utils.config import S3_API_HEADERS
 # Import helper functions
from helpers.data_helpers import get_source_data, get_financial_ratio, get_rules

# Load environment variables from .env.development
load_dotenv('.env.development')
DEFAULT_RULES = os.getenv('DEFAULT_RULES')
@credit_score_bp.route('/', methods=['POST'])
def get_credit_score():
    try:
        request_data = request.json
        document_url = request_data.get('url', None)
        rules_file = request_data.get('rules_file', DEFAULT_RULES)

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
