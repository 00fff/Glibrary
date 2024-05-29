from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from website.apps.auth.auth_views import auth

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY'] = 'Secret_Key'

    # Import blueprints
    from .views import views as main_views
    from .apps.auth import auth_views

    # Register blueprints
    app.register_blueprint(main_views, url_prefix='/')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')  # Register auth Blueprint from auth_views

    return app

