# __init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .financial_ratio import financial_ratio_bp


    app.register_blueprint(financial_ratio_bp, url_prefix='/financial_ratio')

    return app
