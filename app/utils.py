from flask import request
from app.forms import SearchForm

def search_params(request, default_sort='id'):
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    sort = request.args.get('sort', default_sort)
    order = request.args.get('order', 'asc')
    return page, per_page, search, sort, order

def get_page_range(page, per_page, total, range_size=3):
    if total == 0:
        return [1], 1 
    
    total_pages = (total + per_page - 1) // per_page
    start_page = max(1, page - 1)
    end_page = min(total_pages, start_page + (range_size - 1))
    start_page = max(1, end_page - (range_size - 1))
    page_range = list(range(start_page, end_page + 1))
    return page_range, total_pages

def create_search_form(request_args, column_list, search, sort, order):
    form = SearchForm(request_args)
    form.sort.choices = column_list
    form.sort.data = sort
    form.order.data = order
    form.search.data = search
    return form

def create_sort_list(table):
    if table == 'students':
        column_list = [('id', 'Student ID'), ('first_name', 'First Name'),
                        ('last_name', 'Last Name'), ('gender', 'Gender'),
                        ('year_level', 'Year Level'), ('course_code', 'Course Code')]
    elif table == 'program':
        column_list = [('code', 'Course Code'), ('name', 'Course Name'),
                   ('college_code', 'College')]
    elif table == 'college':
        column_list = [('code', 'College Code'), ('name', 'College Name')]
    else:
        column_list = []
        
    return column_list

def create_data_list(table, edit_data):
    if table == 'students':
        data={
            'id': edit_data['id'],
            'first_name': edit_data['first_name'],
            'last_name': edit_data['last_name'],
            'gender': edit_data['gender'],
            'year_level': edit_data['year_level'],
            'course_code': edit_data['course_code']}
    elif table == 'program':
        data={
            'code': edit_data['code'],
            'name': edit_data['name'],
            'college_code': edit_data['college_code']}
    elif table == 'college':
        data={
            'code': edit_data['code'],
            'name': edit_data['name']}
    else:
        data = []
        
    return data