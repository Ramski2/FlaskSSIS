from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SearchField
from wtforms.validators import Length, Email, EqualTo, DataRequired, Regexp

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=3, max=30), DataRequired()])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=8, message='Password must be at least 8 characters long'), DataRequired(), ])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    
    
class StudentForm(FlaskForm):
    id = StringField("Student ID", validators=[DataRequired(), Length(min=9, max=9), Regexp(r'^\d{4}-\d{4}$', message="Student ID must be YYYY-NNNN (e.g. 2025-0001)")])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name")
    gender = SelectField("Gender", choices=[('Male','Male'), ('Female', 'Female'), ('Other', 'Other'), ('Rather not say', 'Rather not say')])
    year_level = SelectField("Year Level", choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], coerce=int)
    course_code = SelectField("Course")
    submit = SubmitField('Add Student')
    
class ProgramForm(FlaskForm):
    code = StringField("Course Code", validators=[DataRequired()])
    name = StringField("Course Name", validators=[DataRequired()])
    college_code = SelectField("College")
    submit = SubmitField('Add Course')
    
class CollegeForm(FlaskForm):
    code = StringField("College Code", validators=[DataRequired()])
    name = StringField("College Name", validators=[DataRequired()])
    submit = SubmitField('Add College')
    
class SearchForm(FlaskForm):
    search = SearchField("Search")
    sort = SelectField("Sort")
    order = SelectField("Order", choices=[("asc", "Ascending"),("desc", "Descending")])
    submit = SubmitField("Search")
    
class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")