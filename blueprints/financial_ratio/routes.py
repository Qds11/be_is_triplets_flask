from . import financial_ratio_bp
from flask import jsonify, request
from .financial_ratio_service import calculate_financial_ratios  # Import the service

@financial_ratio_bp.route('/', methods=['POST'])
def get_financial_ratio():
    request_data = request.json
    source_data = request_data.get('source_data', None)

    if not source_data:
        return jsonify({'error': 'source_data is required'}), 400

    try:
        # Call the service function to calculate the financial ratios
        ratios = calculate_financial_ratios(source_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(ratios), 201
