from flask import Blueprint

college_bp = Blueprint('college', __name__, url_prefix='')

from . import college_routes