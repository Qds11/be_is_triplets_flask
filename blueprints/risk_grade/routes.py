from flask import jsonify, request
from helpers.auth_helpers import admin_api_key_required
from . import risk_grade_bp
from .risk_grade_service import get_risk_grade, fetch_risk_grades, upload_risk_grades_service,update_default_risk_grade

# GET: Fetch risk grade by credit score
@risk_grade_bp.route('/', methods=['GET'])
@admin_api_key_required
def get_risk_grade_api():
    try:
        credit_score = request.args.get('credit_score')
        if not credit_score:
            return jsonify({'error': 'credit score is required'}), 400

        risk_grade_version = request.args.get('risk_grade_version', default=None)
        grade = get_risk_grade(int(credit_score), risk_grade_version)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'credit_score': credit_score, 'risk_grade': grade}), 200


# POST: Upload a new risk grade table
@risk_grade_bp.route('/', methods=['POST'])
@admin_api_key_required
def upload_risk_grade_api():
    try:
        data = request.get_json()
        print(data)
        if not data or 'risk_grades' not in data:
            return jsonify({'error': 'risk_grades data is required'}), 400

        description = data.get('description', '')
        set_default = data.get('set_default', False)

        result = upload_risk_grades_service(data['risk_grades'], description, set_default)
        print("HELP: ",result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(result), 201


# GET: Fetch all risk grades (by version or latest)
@risk_grade_bp.route('/fetch', methods=['GET'])
@admin_api_key_required
def fetch_risk_grades_api():
    try:
        risk_grade_version = request.args.get('risk_grade_version', default=None)
        risk_grades = fetch_risk_grades(risk_grade_version)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(risk_grades), 200


@risk_grade_bp.route('/update-default', methods=['PUT'])
@admin_api_key_required
def update_default_risk_grade_api():
    try:
        data = request.get_json()
        if not data or 'default_risk_file' not in data:
            return jsonify({'error': 'default_risk_file is required'}), 400

        new_default_risk_file = data['default_risk_file']
        result = update_default_risk_grade(new_default_risk_file)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Default risk grade updated', 'new_default': result}), 200
