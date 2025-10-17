from app import app
import app.models as models
from app.forms import RegisterForm, LoginForm, StudentForm, ProgramForm, CollegeForm, SearchForm
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.utils import search_params, get_page_range, create_search_form, create_sort_list, create_data_list

@app.route("/")
def index():
    try:
        students = models.Student.get_all()
        courses = models.Program.get_all()
        colleges = models.College.get_all()
        
        total_st = models.Student.get_count()
        total_cr = models.Program.get_count()
        total_cl = models.College.get_count()
        
        data = models.Student.get_gender_demo()
        labels = [row['course_code']for row in data]
        male_demo = [row['male_count']for row in data]
        female_demo = [row['female_count']for row in data]
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return render_template('index.html', total_st=total_st, total_cr=total_cr, total_cl=total_cl,
                           stds = students, 
                           crs = courses, 
                           clgs = colleges,
                           labels=labels,
                           male_demo=male_demo,
                           female_demo=female_demo)

@app.route("/register", methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = models.User(username=form.username.data, email=form.email.data, password=form.password1.data)
            user.add()
            flash('User created successfully!', 'success')
            return redirect(url_for('login_page'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
        
    return render_template('register.html', form = form)

@app.route("/login", methods=['GET','POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = models.User.get_specific_username(username=form.username.data)
        if attempted_user and attempted_user.check_password(password_attempt=form.password.data):
            login_user(attempted_user, remember=form.remember.data)
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            flash(f"You are now logged in as {current_user.username}", "success")
            return redirect(next_page)
        else:
            flash("Wrong username or password! Please try again", 'danger')
    return render_template('login.html', form=form)
        
@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('index'))

@app.route("/student")
@login_required
def student():
    form = StudentForm()
    table = "students"
    page, per_page, search, sort, order = search_params(request, default_sort='id')

    sort_list = create_sort_list(table)
    search_form = create_search_form(request.args, sort_list, search, sort, order)
    
    
    crs = models.Program.get_all()
    form.course_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in crs]
    
    try:
        students, total = models.Student.get_student_filtered(search,
                                                                  sort, order,
                                                                  page, per_page)
        page_range, total_pages = get_page_range(page, per_page, total)
        
        return render_template('student.html',
                                stds = students, 
                                search=search, 
                                sort=sort, 
                                order=order, 
                                page=page,
                                page_range=page_range,
                                total_pages= total_pages,
                                crs_codes=crs, table = table, form=form,
                                search_form=search_form)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return render_template('student.html',
                               stds=[], search=search, sort=sort,
                               order=order, page=page, page_range=[],
                               total_pages=0, crs_codes=crs, table=table,
                               form=form, search_form=search_form)

@app.route("/program")
@login_required
def course():
    form = ProgramForm()
    table = "program"
    page, per_page, search, sort, order = search_params(request, default_sort='code')

    sort_list = create_sort_list(table)
    search_form = create_search_form(request.args, sort_list, search, sort, order)
    
    clg = models.College.get_all()
    form.college_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in clg]
    try:
        courses, total = models.Program.get_program_filtered(search, sort, order, page, per_page)
        page_range, total_pages = get_page_range(page, per_page, total)
        
        return render_template('program.html',
                               crs=courses, 
                               search=search, 
                               sort=sort, 
                               order=order, 
                               page=page,
                               page_range=page_range,
                               total_pages= total_pages,
                               clg_codes=clg, table = table, form=form,
                               search_form=search_form)
    except Exception as e:
         flash(f"Error: {str(e)}", "danger")
         return render_template('program.html',
                               crs=[], 
                               search=search, 
                               sort=sort, 
                               order=order, 
                               page=page,
                               page_range=[],
                               total_pages= 0,
                               clg_codes=clg, table = table, form=form,
                               search_form=search_form)

@app.route("/college")
@login_required
def college():
    form = CollegeForm()
    table = "college"
    page, per_page, search, sort, order = search_params(request, default_sort='code')

    sort_list = create_sort_list(table)
    search_form = create_search_form(request.args, sort_list, search, sort, order)
    try:
        colleges, total = models.College.get_college_filtered(search, sort, order, page, per_page)
        page_range, total_pages = get_page_range(page, per_page, total)
        
        return render_template('college.html',
                               clgs=colleges, 
                               search=search, 
                               sort=sort, 
                               order=order, 
                               page=page,
                               page_range=page_range,
                               total_pages= total_pages, table = table,
                               form=form, search_form=search_form)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return render_template('college.html',
                               clgs=[], 
                               search=search, 
                               sort=sort, 
                               order=order, 
                               page=page,
                               page_range=[],
                               total_pages= 0, table = table,
                               form=form, search_form=search_form)

@app.route("/student/add", methods=["GET", "POST"])
@login_required
def add_std():
    form = StudentForm()
    crs = models.Program.get_all()
    form.course_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in crs]
    if form.validate_on_submit():   
        try:
            student = models.Student(form.id.data,
                                     form.first_name.data, 
                                     form.last_name.data, 
                                     form.gender.data, 
                                     form.year_level.data, 
                                     form.course_code.data)
            student.add()
            flash('Student Added Successfully!', "success")
            return redirect(url_for('student'))
        except Exception as e:
            app.logger.error(f"Error adding student: {e}")
            flash("An error occurred while adding the student.", "danger")
            return redirect(url_for('student'))
    else:
        flash("Please correct the errors in the form.", "warning")
        return redirect(url_for('student'))

@app.route("/student/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_std(id):
    
    edit_data = models.Student.get_specific_student(id)
    if not edit_data:
        flash("Student not found", "danger")
        return redirect(url_for('student'))
    data = create_data_list('students', edit_data)
    form = StudentForm()
    crs = models.Program.get_all()
    form.submit.label.text = "Edit Student"
    form.course_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in crs]
    if form.validate_on_submit():
        try:
            models.Student.update(id, form.id.data,
                                  form.first_name.data,
                                  form.last_name.data,
                                  form.gender.data,
                                  form.year_level.data,
                                  form.course_code.data)
            flash('Student Updated Successfully!', 'success')
            return redirect(url_for('student'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    else:
        return render_template("edit.html", table="student", edit_data=edit_data, crs_codes=crs, id=id, form=form)
 
@app.route("/student/delete/<id>")
@login_required
def del_std(id):
    try:
        models.Student.delete(id)
        flash('Student Deleted Successfully!', 'success')
        return redirect(url_for('student'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

@app.route("/program/add", methods=["GET", "POST"])
@login_required
def add_crs():
    form = ProgramForm()
    clg = models.College.get_all()
    form.college_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in clg]

    if form.validate_on_submit():
        try:
            course = models.Program(form.code.data,
                                    form.name.data, 
                                    form.college_code.data)
            course.add()
            next_url = request.form.get('next') or url_for('course')
            flash('Added Successfully!', "success")
            return redirect(next_url)
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    else:
        clg = models.College.get_all()
        next_url = request.args.get('next', url_for('course'))
        return render_template("add.html", table="course", clg_codes=clg, next=next_url, form=form)

@app.route("/program/edit/<code>", methods=["POST","GET"])
@login_required
def edit_crs(code):
    edit_data = models.Program.get_specific_program(code)
    form = ProgramForm(data={
            'code': edit_data['code'],
            'name': edit_data['name'],
            'college_code': edit_data['college_code']})
    clg = models.College.get_all()
    form.submit.label.text = "Edit Course"
    form.college_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in clg]
    
    if form.validate_on_submit():  
        try:
            models.Program.update(code, form.code.data, form.name.data, form.college_code.data)
            flash('Edited Successfully!', "success")
            return redirect(url_for('course'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    else:
        return render_template("edit.html", table="course", edit_data=edit_data, clg_codes=clg, form=form)

@app.route("/program/delete/<code>")
@login_required
def del_crs(code):
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'code')
    order = request.args.get('order', 'asc')
    try:
        models.Program.delete(code)
        flash('Deleted Successfully!', "success")
        return redirect(url_for('course', page=page, search=search, sort=sort, order=order))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

@app.route("/college/add", methods=["GET", "POST"])
@login_required
def add_clg():
    form = CollegeForm()
    if form.validate_on_submit():            
        try:
            college = models.College(form.code.data, form.name.data)
            college.add()
            next_url = request.form.get('next') or url_for('college')
            flash('Added Successfully!', "success")
            return redirect(next_url)
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    else:
        next_url = request.args.get('next', url_for('college'))
        return render_template("add.html", table="college", next=next_url, form=form)

@app.route("/college/edit/<code>", methods=["GET", "POST"])
@login_required
def edit_clg(code):
    edit_data = models.College.get_specific_college(code)
    form = ProgramForm(data={
            'code': edit_data['code'],
            'name': edit_data['name']})
    form.submit.label.text = "Edit Course"
    if form.validate_on_submit():
        try:
            models.College.update(code, form.code.data, form.name.data)
            flash('Edited Successfully!', "success")
            return redirect(url_for('college'))
            
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    else:
        return render_template("edit.html", table="college", edit_data=edit_data, form=form)


@app.route("/college/delete/<code>")
@login_required
def del_clg(code):
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'code')
    order = request.args.get('order', 'asc')
    try:
        models.College.delete(code)
        flash('Deleted Successfully!', "success")
        return redirect(url_for('college', page=page, search=search, sort=sort, order=order))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")