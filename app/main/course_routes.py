from flask import flash, jsonify, render_template, request, url_for
from flask_login import login_required
from app import models
from app.forms import ProgramForm
from app.utils import create_sort_list, get_page_range, search_params, create_data_list
from . import main_bp

@main_bp.route("/program")
@login_required
def course():
    form = ProgramForm()
    table = "program"
    sort_list = create_sort_list(table)
    
    clg = models.College.get_all()
    form.college_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in clg] 
    
    return render_template('program.html',
                               clg_codes=clg, table = table, form=form,
                               sort_list=sort_list)
         
@main_bp.route("/program/table")
@login_required
def load_courses_filtered():
    page, per_page, search, sort, order = search_params(request, default_sort='code')

    courses, total = models.Program.get_program_filtered(search, sort, order, page, per_page)
    page_range, total_pages = get_page_range(page, per_page, total)
    
    table_html = render_template("partials/program_table.html", crs=courses, page=page, editable=True)
    paging_html = render_template("includes/pagination.html", table="program", page=page, page_range=page_range,
                                      total_pages=total_pages,
                                      search=search,
                                      sort=sort,
                                      order=order)

    return jsonify({
        "table": table_html,
        "pagination": paging_html
    })

@main_bp.route("/program/add", methods=["GET", "POST"])
@login_required
def add_crs():
    form = ProgramForm()
    clg = models.College.get_all()
    form.college_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in clg]

    url = "/program/add"
    next_url = request.args.get('next') or url_for('main.student')
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                course = models.Program(form.code.data,
                                        form.name.data, 
                                        form.college_code.data)
                course.add()
                return jsonify(success=True, message="Course added successfully!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400
    else:
        return render_template('add.html', form=form, table='program', next_url=next_url, url=url)    


@main_bp.route("/program/edit/<code>", methods=["PUT","GET"])
@login_required
def edit_crs(code):
    edit_data = models.Program.get_specific_program(code)
    data = create_data_list("program", edit_data)
    form = ProgramForm(data=data)
    clg = models.College.get_all()
    form.submit.label.text = "Edit Course"
    form.college_code.choices = [(c['code'], f"{c['code']} - {c['name']}") for c in clg]
    if request.method == "PUT":
        if form.validate_on_submit():  
            try:
                models.Program.update(code, form.code.data, form.name.data, form.college_code.data)
                return jsonify(success=True, message="Course updated successfully!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400

    return render_template('includes/program_form.html', form=form, table='program')

@main_bp.route("/program/delete/<code>", methods=["DELETE"])
@login_required
def del_crs(code):
    try:
        models.Program.delete(code)
        return jsonify({'success': True, 'message': 'College deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500