from flask import Flask  # Import Flask for creating the Flask application
from flask_restful import Api  # Import Flask-RESTful for creating RESTful APIs
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM (Object-Relational Mapping)
from .views import views as main_views  # Import the main views from your views module and rename them to main_views
from flask_migrate import Migrate  # Import Flask-Migrate for handling database migrations
from .apps.auth import auth_views  # Import auth views from your auth module
from .apps.data import data_views  # Import data views from your data module
from .database import db  # Import db from your database module
from flask_login import LoginManager, UserMixin  # Import Flask-Login for user session management
from datetime import timedelta  # Import timedelta for setting session lifetime
from website.apps.share_models import Game, User  # Import shared models (Game and User) from your models module
from website.apps.cache_config import cache
from flask_mail import Mail, Message
import os 
from website.apps.mail import mail

# Initialize the cache at the top level


def create_app():
    app = Flask(__name__, template_folder="templates")  # Initialize Flask app with the specified templates folder
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # Set the database URI for SQLAlchemy (fixed typo)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy track modifications (recommended for performance)
    app.config['SECRET_KEY'] = 'Secret_Key'  # Set the secret key for session management and other security needs
    app.permanent_session_lifetime = timedelta(days=30)  # Set session lifetime to 30 days
    app.static_folder = 'static'  # Specify the folder for static files
    
    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    # Initialize Flask-Migrate with the Flask app and SQLAlchemy db instance
    migrate = Migrate(app, db)
    
    # Register blueprints for different parts of the app
    app.register_blueprint(main_views, url_prefix='/')  # Register main views with root URL prefix
    app.register_blueprint(auth_views.auth, url_prefix='/auth')  # Register auth views with /auth URL prefix
    app.register_blueprint(data_views.data, url_prefix='/data')  # Register data views with /data URL prefix
    
    return app  # Return the Flask app instance
