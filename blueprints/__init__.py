# __init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .financial_ratio import financial_ratio_bp
    from .source_data import source_data_bp
    from .credit_score import credit_score_bp
    from .credit_score_rules import credit_score_rules_bp


    app.register_blueprint(financial_ratio_bp, url_prefix='/financial-ratio')
    app.register_blueprint(source_data_bp, url_prefix='/source-data')
    app.register_blueprint(credit_score_bp, url_prefix='/credit-score')
    app.register_blueprint(credit_score_rules_bp, url_prefix='/credit-score-rules')

    return app
