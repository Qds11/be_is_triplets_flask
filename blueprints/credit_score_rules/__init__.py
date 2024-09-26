# blueprints/main/__init__.py
from flask import Blueprint
from flask_restful import Api, Resource
credit_score_rules_bp = Blueprint('credit_score_rules', __name__)
from . import routes
api = Api(credit_score_rules_bp)

class CreditScoreRulesResource(Resource):
    def get(self):
        return {"message": "Credit score rules data"}

api.add_resource(CreditScoreRulesResource, '/')




