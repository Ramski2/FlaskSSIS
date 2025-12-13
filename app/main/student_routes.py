from flask import flash, jsonify, render_template, request, url_for
from flask_login import login_required
from app import models
from app.forms import StudentForm
import cloudinary
import cloudinary.uploader
from app.utils import create_data_list, create_sort_list, get_page_range, search_params
from . import main_bp

DEFAULT_IMAGE_URL = "https://res.cloudinary.com/demo/image/upload/v1699481234/default-image.png"
DEFAULT_PUBLIC_ID = "default-image"

@main_bp.route("/student")
@login_required
def student():
    form = StudentForm()
    table = "students"
    last_id = models.Student.get_last()
    next_id = models.Student.increment_id(last_id)
    
    form.id.data = next_id
    sort_list = create_sort_list(table)

    crs = models.Program.get_all()
    form.course_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in crs]
        
    return render_template('student.html',
                                crs_codes=crs, table = table, form=form,
                                sort_list=sort_list)
        
   
   
@main_bp.route("/student/table")
@login_required
def load_students_filtered():
    page, per_page, search, sort, order = search_params(request, default_sort='id')

    students, total = models.Student.get_student_filtered(search, sort, order, page, per_page)
    page_range, total_pages = get_page_range(page, per_page, total)
    
    table_html = render_template("partials/student_table.html", stds=students, page=page, editable=True)
    paging_html = render_template("includes/pagination.html",page=page, page_range=page_range,
                                      total_pages=total_pages,
                                      search=search,
                                      sort=sort,
                                      order=order, table="students")
    return jsonify({
        "table": table_html,
        "pagination": paging_html
    })
         
@main_bp.route("/student/add", methods=["GET", "POST"])
@login_required
def add_std():
    form = StudentForm()
    crs = models.Program.get_all()
    url = "/student/add"
    
    last_id = models.Student.get_last()
    next_id = models.Student.increment_id(last_id)
    
    form.id.data = next_id
    print(form.id.data)
    form.course_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in crs]

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # Check if ID exists
                if models.Student.get_specific_student(form.id.data):
                    return jsonify(success=False, error="ID number already exists."), 409

                # File upload
                file = form.image.data
                result = cloudinary.uploader.upload(file)
                image_url = result.get("secure_url")
                public_id = result.get("public_id")


                # Create student
                student = models.Student(
                    form.id.data,
                    image_url,
                    public_id,
                    form.first_name.data,
                    form.last_name.data,
                    form.gender.data,
                    form.year_level.data,
                    form.course_code.data
                )
                student.add()

                return jsonify(success=True, message="Student added successfully!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400

    return render_template('add.html', form=form, table='students', url="/student/add")


@main_bp.route("/student/edit/<id>", methods=["GET", "PUT"])
@login_required
def edit_std(id):
    edit_data = models.Student.get_specific_student(id)
    if not edit_data:
        return jsonify(success=False, error="Student not found"), 404
    
    data = create_data_list('students', edit_data)
    form = StudentForm(data=data)
    crs = models.Program.get_all()
    form.submit.label.text = "Edit Student"
    form.course_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in crs]
    
    if request.method == "PUT":
        if form.validate_on_submit():
            try:
 
                file = form.image.data
                result = cloudinary.uploader.upload(file)
                image_url = result.get("secure_url")
                public_id = result.get("public_id")
                
                models.Student.update(id, form.id.data,
                                    image_url,
                                    public_id,
                                    form.first_name.data,
                                    form.last_name.data,
                                    form.gender.data,
                                    form.year_level.data,
                                    form.course_code.data)
                return jsonify(success=True, message="Student updated successfully!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400

    return render_template('includes/student_form.html', form=form, student=edit_data, table='students')
 
@main_bp.route("/student/delete/<id>", methods=["DELETE"])
@login_required
def del_std(id):
    try:
        models.Student.delete(id)
        return jsonify(success= True, message='Student deleted successfully.')
    except Exception as e:
        return jsonify(success=False, error= str(e)), 500