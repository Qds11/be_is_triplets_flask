from blueprints.source_data.source_data_service import ocr_method as source_data_service
from blueprints.financial_ratio.financial_ratio_service import calculate_financial_ratios
from blueprints.credit_score_rules.rules_service import fetch_rules  # Assuming this is the service method for fetching rules
from blueprints.risk_grade.risk_grade_service import get_risk_grade as get_risk_grade_service  # Assuming this is the service method for fetching rules

# Helper function to get source data
def get_source_data(urls):
    try:
        # Attempt to get the source data using the service method
        source_data = source_data_service(urls)
        return source_data
    except Exception as e:
        # Catch any exceptions and raise a meaningful error
        raise Exception(f"Could not retrieve source data: {str(e)}")

# Helper function to get financial ratios
def get_financial_ratio(source_data):
    try:
        # Call the service function instead of making an HTTP request
        financial_ratios = calculate_financial_ratios(source_data)
        return financial_ratios
    except Exception as e:
        raise Exception(f"Could not retrieve financial ratio: {str(e)}")

# Helper function to get financial ratios
def get_risk_grade(credit_score):
    try:
        # Call the service function instead of making an HTTP request
        risk_grade = get_risk_grade_service(credit_score)
        return risk_grade
    except Exception as e:
        raise Exception(f"Could not retrieve risk grade: {str(e)}")

# Helper function to get rules
def get_rules(rules_version=None):
    try:
        # Call the service function instead of making an HTTP request
        rules = fetch_rules(rules_version)
        return rules
    except Exception as e:
        raise Exception(f"Could not retrieve credit score rules: {str(e)}")
