from flask import Blueprint

main_bp = Blueprint('main', __name__, url_prefix='')

from . import home_route, student_routes, course_routes, college_routes