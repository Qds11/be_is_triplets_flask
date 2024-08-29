# blueprints/main/routes.py
from . import financial_ratio_bp

@financial_ratio_bp.route('/', methods=['POST'])
def get_financial_ratio():
    return "hello"
