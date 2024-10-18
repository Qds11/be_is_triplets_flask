from flask import jsonify, request

from helpers.auth_helpers import admin_api_key_required
from helpers.error_helpers import handle_error

from ..credit_score_rules.rules_service import (fetch_rules, get_all_rules,
                                                update_default_rules,
                                                upload_rules_service)
from . import credit_score_rules_bp


@credit_score_rules_bp.route('/fetch', methods=['GET'])
@admin_api_key_required
def get_credit_score_rules():
    rules_version = request.args.get('rules_version', default=None)
    try:
        rules = fetch_rules(rules_version)
        return jsonify(rules), 200
    except Exception as e:
        return handle_error(f"Error fetching rules: {str(e)}", 500)

@credit_score_rules_bp.route('/default-rules/update', methods=['POST'])
@admin_api_key_required
def update_default_rules_route():
    try:
        new_default_rules_version = request.json.get('rules_version')
        updated_rules = update_default_rules(new_default_rules_version)
        return jsonify({'message': 'Default rules file updated', 'new_default_rules_version': updated_rules}), 200
    except Exception as e:
        return handle_error(f"Error updating default rules: {str(e)}", 500)

@credit_score_rules_bp.route('/upload', methods=['POST'])
@admin_api_key_required
def upload_rules_route():
    try:
        rules = request.json.get('rules')
        description = request.json.get('description', '')
        set_default = request.json.get('set_default', False)

        if not rules:
            return handle_error('Data for rules file is required', 400)

        response = upload_rules_service(rules, description, set_default)
        return jsonify(response), 201
    except Exception as e:
        return handle_error(f"Error uploading rules file: {str(e)}", 500)

@credit_score_rules_bp.route('/', methods=['GET'])
@admin_api_key_required
def get_all_rules_route():
    try:
        rules_files = get_all_rules()
        return jsonify(rules_files), 200
    except Exception as e:
        return handle_error(f"Error getting rules files: {str(e)}", 500)
