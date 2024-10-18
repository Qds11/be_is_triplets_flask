# blueprints/main/__init__.py
from flask import Blueprint
from flask_restful import Api, Resource
risk_grade_bp = Blueprint('risk_grade', __name__)
from . import routes
api = Api(risk_grade_bp)

class RiskGradeResource(Resource):
    def get(self):
        return {"message": "Risk grade data"}

api.add_resource(RiskGradeResource, '/')
