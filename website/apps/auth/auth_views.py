from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__, template_folder='templates/auth')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template('log_out.html')

@auth.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    return render_template('sign_up.html')