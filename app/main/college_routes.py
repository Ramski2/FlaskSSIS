from flask import flash, jsonify, render_template, request, url_for
from flask_login import login_required
from app import models
from app.forms import CollegeForm
from app.utils import create_sort_list, get_page_range, search_params, create_data_list
from . import main_bp

@main_bp.route("/college")
@login_required
def college():
    form = CollegeForm()
    table = "college"
    sort_list = create_sort_list(table)
    
    return render_template('college.html',
                               table = table,
                               form=form, sort_list=sort_list)
        
@main_bp.route("/college/table")
@login_required
def load_colleges_filtered():
    page, per_page, search, sort, order = search_params(request, default_sort='code')
    
    colleges, total = models.College.get_college_filtered(search, sort, order, page, per_page)
    page_range, total_pages = get_page_range(page, per_page, total)
    
    table_html = render_template("partials/college_table.html", clgs=colleges, page=page, editable=True)
    paging_html = render_template("includes/pagination.html",page=page, page_range=page_range,
                                      total_pages=total_pages,
                                      search=search,
                                      sort=sort,
                                      order=order, table="college")
    return jsonify({
        "table": table_html,
        "pagination": paging_html
    })

        
@main_bp.route("/college/add", methods=["GET", "POST"])
@login_required
def add_clg():
    form = CollegeForm()
    
    next_url = request.args.get('next') or url_for('main.course')
    url = "/college/add"
    
    if request.method == "POST":
        if form.validate_on_submit():            
            try:
                existing_code = models.College.get_specific_college(form.code.data)
                if existing_code:
                    return jsonify(success=False, error="College Code already exists."), 409
                
                existing_name = models.College.get_specific_college_name(form.name.data)
                if existing_name:
                    return jsonify(success=False, error="College name already exists."), 409
                
                college = models.College(form.code.data, form.name.data)
                college.add()
                return jsonify(success=True, message="College added successfully!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400
    else:
        return render_template('add.html', form=form, table='college', next_url=next_url, url=url)  

@main_bp.route("/college/edit/<code>", methods=["GET", "PUT"])
@login_required
def edit_clg(code):
    edit_data = models.College.get_specific_college(code)
    data = create_data_list("college", edit_data)
    form = CollegeForm(data=data)
    form.submit.label.text = "Edit College"
    if request.method == "PUT":
        if form.validate_on_submit():
            try:
                models.College.update(code, form.code.data, form.name.data)
                
                return jsonify(success=True, message="College updated successfully!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400

    return render_template('includes/college_form.html', form=form, table='college')


@main_bp.route("/college/delete/<code>", methods=["DELETE"])
@login_required
def del_clg(code):
    try:
        models.College.delete(code)
        return jsonify({'success': True, 'message': 'College deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500