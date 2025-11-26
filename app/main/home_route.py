from flask import flash, render_template
from app import models
from . import main_bp

@main_bp.route("/")
def index():
    return render_template('index.html')
    
@main_bp.route("/test")
def test():
    students = models.Student.get_all()
    courses = models.Program.get_all()
    colleges = models.College.get_all()
    return render_template('test.html', stds = students, 
                           crs = courses, 
                           clgs = colleges)