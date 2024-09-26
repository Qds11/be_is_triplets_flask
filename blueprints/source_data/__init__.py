# blueprints/main/__init__.py
from flask import Blueprint
from flask_restful import Api, Resource
source_data_bp = Blueprint('source_data', __name__)
from . import routes
api = Api(source_data_bp)

class SourceDataResource(Resource):
    def get(self):
        return {"message": "source data"}

api.add_resource(SourceDataResource, '/')




