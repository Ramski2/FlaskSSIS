from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT, SECRET_KEY, cloud_name, api_key, api_secret
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from . import database
import cloudinary
import cloudinary.uploader


login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()
bootstrap = Bootstrap()

def create_app():
    app =Flask(__name__,  instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = SECRET_KEY,
        DATABASE_URL=f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
    
    cloudinary.config(
        cloud_name = cloud_name,
        api_key = api_key,
        api_secret = api_secret,
        secure=True
    )
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    
    
    login_manager.login_view = "user.login_page"
    login_manager.login_message_category = "Please log in to access this page"
    
    from .user import user_bp
    from .main import main_bp
    from .student import student_bp
    from .course import course_bp
    from .college import college_bp
    
    
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(college_bp)
    
    return app