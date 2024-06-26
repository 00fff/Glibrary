from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .views import views as main_views
from flask_migrate import Migrate
from .apps.auth import auth_views
from .apps.data import data_views
from .database import db
from flask_login import LoginManager, UserMixin
from datetime import timedelta
from dotenv import load_dotenv
from website.apps.share_models import Game, User, UserGame
from website.apps.cache_config import cache
from website.mail_config import mail  # Import mail from mail_config.py
import os

def create_app():
    load_dotenv()  # Load environment variables from .env file
    app = Flask(__name__, template_folder="templates")
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ucp6ml06ju39d:pa1a7e71f5f3d78d13572661d7346cbc31c8f04d529b53ec694f8fe01a5917565@c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6k5i827jr8gq2'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
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
    cache.init_app(app)
    mail.init_app(app)  # Initialize mail with the app

    migrate = Migrate(app, db)

    app.register_blueprint(main_views, url_prefix='/')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')
    app.register_blueprint(data_views.data, url_prefix='/data')

    return app

