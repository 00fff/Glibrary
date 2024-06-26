from flask_mail import Message
from website.mail_config import mail
from flask import current_app

home_email = "00fffprojects@gmail.com"

def send_email(subject, recipient, body, html_body=None):
    msg = Message(subject, sender=home_email, recipients=[recipient])
    msg.body = body
    if html_body:
        msg.html = html_body
    with current_app.app_context():
        mail.send(msg)
