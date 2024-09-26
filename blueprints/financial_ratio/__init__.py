# blueprints/main/__init__.py
from flask import Blueprint
from flask_restful import Api, Resource
financial_ratio_bp = Blueprint('financial_ratio', __name__)
from . import routes
api = Api(financial_ratio_bp)

class FinancialRatioResource(Resource):
    def get(self):
        return {"message": "Financial ratio data"}

api.add_resource(FinancialRatioResource, '/')
