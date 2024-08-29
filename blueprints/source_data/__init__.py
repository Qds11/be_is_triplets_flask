# blueprints/main/__init__.py
from flask import Blueprint

source_data_bp = Blueprint('source_data', __name__)

from . import routes
