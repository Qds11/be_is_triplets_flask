# blueprints/main/__init__.py
from flask import Blueprint

credit_score_bp = Blueprint('credit_score', __name__)

from . import routes
