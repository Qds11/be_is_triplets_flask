import requests
from flask import jsonify, url_for

# Helper function to get source data
def get_source_data(document_url):
    source_data_url = url_for('source_data.get_source_data', _external=True)

    # Make a POST request to the source_data route with the document_id
    response = requests.post(source_data_url, json={'url': document_url})
    if response.status_code == 200:
        source_data = response.json()
        return source_data
    else:
        return jsonify({'error': 'Could not retrieve source data'}), response.status_code

# Helper function to get financial ratios
def get_financial_ratio(source_data):
    financial_ratio_url = url_for('financial_ratio.get_financial_ratio', _external=True)

    # Make a POST request to the financial_ratio route with the source_data
    response = requests.post(financial_ratio_url, json={'source_data': source_data})
    if response.status_code == 200:
        financial_ratio = response.json()
        return financial_ratio
    else:
        return jsonify({'error': 'Could not retrieve financial ratio'}), response.status_code

# Helper function to get rules
def get_rules(rules_file):
    rules_url = url_for('credit_score_rules.get_credit_score_rules', _external=True)

    # Make a POST request to the rules route with the rules_file
    response = requests.post(rules_url, json={'rules_file': rules_file})
    if response.status_code == 200:
        rules = response.json()
        return rules
    else:
        return jsonify({'error': 'Could not retrieve rules'}), response.status_code
