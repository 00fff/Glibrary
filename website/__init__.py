from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import views as main_views
from .apps.auth import auth_views
from .database import db  # Import db from your database module
from flask_login import LoginManager
from datetime import timedelta

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # Fix typo in the URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'Secret_Key'
    app.permanent_session_lifetime = timedelta(days=30)
    
    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)
    # Initialize Flask-Login
    
    # Register blueprints
    app.register_blueprint(main_views, url_prefix='/')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')

    with app.app_context():
        # Create the database tables
        db.create_all()

    return app
