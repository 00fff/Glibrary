from flask_mail import Mail
from flask import Flask
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Configure Flask-Mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'mawt3ni@gmail.com'
    app.config['MAIL_PASSWORD'] = 'pdtbehhjlgzlvafi '

    # Initialize Flask-Mail with the Flask app
    mail.init_app(app)

    return app