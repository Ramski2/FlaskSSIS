from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import models
from app.forms import LoginForm, RegisterForm
from . import user_bp

@user_bp.route("/login", methods=['GET','POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = models.User.get_specific_username(username=form.username.data)
        if attempted_user and attempted_user.check_password(password_attempt=form.password.data):
            login_user(attempted_user, remember=form.remember.data)
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            flash(f"You are now logged in as {current_user.username}", "success")
            return redirect(next_page)
        else:
            flash("Wrong username or password! Please try again", 'danger')
    return render_template('login.html', login_form=form)

@user_bp.route("/register", methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    url = "/register"
    next_url = "/login"
    
    if request.method == "POST":
        if form.validate_on_submit():   
            try:
                existing_user = models.User.get_specific_username(form.username.data)
                if existing_user:
                    return jsonify(success=False, error="Username already exists."), 409
                
                existing_email = models.User.get_specific_email(form.email.data)
                if existing_email:
                    return jsonify(success=False, error="Email already exists."), 409
                
                user = models.User(username=form.username.data, email=form.email.data, password=form.password1.data)
                user.add()
                return jsonify(success=True, message="Account created!")
            except Exception as e:
                return jsonify(success=False, error=str(e)), 500
        else:
            return jsonify(success=False, errors=form.errors), 400
    else:
        return render_template('register.html', form=form, url=url, next_url=next_url)    


@user_bp.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('main.index'))