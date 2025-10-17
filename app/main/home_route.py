from flask import flash, render_template
from app import models
from . import main_bp

@main_bp.route("/")
def index():
    try:

        students = models.Student.get_all()
        courses = models.Program.get_all()
        colleges = models.College.get_all()
        
        total_st = models.Student.get_count()
        total_cr = models.Program.get_count()
        total_cl = models.College.get_count()
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        
    return render_template('index.html', total_st=total_st, total_cr=total_cr, total_cl=total_cl,
                           stds = students, 
                           crs = courses, 
                           clgs = colleges)
    
@main_bp.route("/test")
def test():
    students = models.Student.get_all()
    courses = models.Program.get_all()
    colleges = models.College.get_all()
    return render_template('test.html', stds = students, 
                           crs = courses, 
                           clgs = colleges)