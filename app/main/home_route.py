from flask import flash, jsonify, render_template
from app import models
from . import main_bp

@main_bp.route("/")
def index():
    try:

        students = models.Student.get_all()
        courses = models.Program.get_all()
        colleges = models.College.get_all()
        
        total_students = models.Student.get_count()
        total_courses = models.Program.get_count()
        total_colleges = models.College.get_count()
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        
    return render_template('index.html',
                           stds = students, 
                           crs = courses, 
                           clgs = colleges,
                           total_students = total_students,
                           total_courses = total_courses,
                           total_colleges = total_colleges)
    
    
@main_bp.route("/index/student/table")
def load_students():
    students = models.Student.get_all()
    
    table_html = render_template("partials/student_table.html", stds=students, editable=False)
    return jsonify({
        "table": table_html
    })
    

@main_bp.route("/index/college/table")
def load_college():
    colleges= models.College.get_all()
    
    table_html = render_template("partials/college_table.html", clgs=colleges, editable=False)
    return jsonify({
        "table": table_html
    })

@main_bp.route("/index/program/table")
def load_colleges():
    courses= models.Program.get_all()
    
    table_html = render_template("partials/program_table.html", crs=courses, editable=False)
    return jsonify({
        "table": table_html
    })

@main_bp.route("/test")
def test():
    students = models.Student.get_all()
    courses = models.Program.get_all()
    colleges = models.College.get_all()
    
    total_students = models.Student.get_count()
    total_courses = models.Program.get_count()
    total_colleges = models.College.get_count()
    return render_template('test.html', stds = students, 
                           crs = courses, 
                           clgs = colleges,
                           total_students = total_students,
                           total_courses = total_courses,
                           total_colleges = total_colleges)
    