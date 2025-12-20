from flask import Blueprint

course_bp = Blueprint('course', __name__, url_prefix='')

from . import course_routes