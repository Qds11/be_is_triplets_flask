# blueprints/main/__init__.py
from flask import Blueprint

financial_ratio_bp = Blueprint('financial_ratio', __name__)

from . import routes
