# __init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .financial_ratio import financial_ratio_bp
    from .source_data import source_data_bp
    from .credit_score import credit_score_bp


    app.register_blueprint(financial_ratio_bp, url_prefix='/financial_ratio')
    app.register_blueprint(source_data_bp, url_prefix='/source_data')
    app.register_blueprint(credit_score_bp, url_prefix='/credit_score')

    return app
