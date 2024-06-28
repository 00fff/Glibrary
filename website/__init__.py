# website/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from dotenv import load_dotenv
from datetime import timedelta
import os

from website.database import db
mail = Mail()
cache = Cache()

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder="templates")
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://glibrary_postgres_user:onxXhcrJaMgdK0TwSe2TK4DuZOoxdc5S@dpg-cpua6caju9rs73fv9u20-a.oregon-postgres.render.com/glibrary_postgres'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['UPLOAD_DIRECTORY'] = "uploads/"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEBUG'] = False
    app.permanent_session_lifetime = timedelta(days=30)
    app.static_folder = 'static'

    db.init_app(app)
    mail.init_app(app)
    # cache.init_app(app)

    
    from website.apps.auth import auth_views
    from website.apps.data import data_views
    from website.views import views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')
    app.register_blueprint(data_views.data, url_prefix='/data')

    return app
