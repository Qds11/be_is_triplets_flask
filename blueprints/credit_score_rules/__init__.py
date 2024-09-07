# blueprints/main/__init__.py
from flask import Blueprint

credit_score_rules_bp = Blueprint('credit_score_rules', __name__)

from . import routes
