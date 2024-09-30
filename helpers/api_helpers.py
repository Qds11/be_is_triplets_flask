import requests
from flask import url_for
import json
# Helper function to get source data
def get_source_data(urls):
    source_data_url = url_for('source_data.get_source_data', _external=True)

    response = requests.post(source_data_url, json={'urls': urls})

    if response.status_code != 200:
        raise Exception(f"Could not retrieve source data, status code: {response.status_code}")
    try:
        source_data = response.json()
        return source_data
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON from response: {str(e)}")

# Helper function to get financial ratios
def get_financial_ratio(source_data):
    financial_ratio_url = url_for('financial_ratio.get_financial_ratio', _external=True)

    response = requests.post(financial_ratio_url, json={'source_data': source_data})

    if response.status_code != 200:
        error_message = response.json().get('error', 'Unknown error')  # Extracting just the error message
        raise Exception(f"Could not retrieve financial ratio, status code: {response.status_code}, error: {error_message}")
    try:
        financial_ratio = response.json()
        return financial_ratio
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON from response: {str(e)}")

# Helper function to get rules
def get_rules(rules_version):

    try:
        rules_url = url_for('credit_score_rules.get_credit_score_rules', _external=True, rules_version=rules_version)
        # Make a POST request to the rules route with the rules_file
        response = requests.get(rules_url)
    except:
        # Raise the exception with the extracted error message
        error_message = response.json().get('error', 'Unknown error')
        raise Exception(f"Could not retrieve credit score rules, status code: {response.status_code}, error: {error_message}")

    # Parse the JSON response
    try:
        rules = response.json()
        return rules
    except json.JSONDecodeError as e:
        raise Exception(f"Could not retrieve credit score rules: Failed to parse JSON from response ({str(e)})")
