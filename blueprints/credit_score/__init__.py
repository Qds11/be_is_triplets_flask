# blueprints/main/__init__.py
from flask import Blueprint
from flask_restful import Api, Resource
credit_score_bp = Blueprint('credit_score', __name__)
from . import routes
api = Api(credit_score_bp)

class CreditScoreResource(Resource):
    def get(self):
        return {"message": "Credit score data"}

api.add_resource(CreditScoreResource, '/')

