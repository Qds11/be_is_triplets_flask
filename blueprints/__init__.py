# __init__.py
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (localhost:5000/swagger)
    API_DOCS_URL = '/static/swagger.json'  # Path to your Swagger API specification file

    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files route
    API_DOCS_URL,  # API documentation URL
    config={  # Swagger UI config overrides
        'app_name': "Credit Evaluation"
    }
)
    from .financial_ratio import financial_ratio_bp
    from .source_data import source_data_bp
    from .credit_score import credit_score_bp
    from .credit_score_rules import credit_score_rules_bp
    from .risk_grade import risk_grade_bp

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(financial_ratio_bp, url_prefix='/financial-ratio')
    app.register_blueprint(source_data_bp, url_prefix='/source-data')
    app.register_blueprint(credit_score_bp, url_prefix='/credit-score')
    app.register_blueprint(credit_score_rules_bp, url_prefix='/credit-score-rules')
    app.register_blueprint(risk_grade_bp, url_prefix='/risk-grade')

    return app
