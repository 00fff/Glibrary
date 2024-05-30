from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from website.database import db

auth = Blueprint('auth', __name__, template_folder='templates/auth')

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(password=password, email=email).first()
        if existing_user:
            # Store username and email in session
            session['username'] = existing_user.username
            session['email'] = existing_user.email
            # Redirect to the user page
            return redirect(url_for('auth.user'))
        else:
            return redirect(url_for('auth.sign_up'))
    # If the user navigates directly to the login page, provide a default value for username
    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Clear session variables
    session.pop("username", None)
    session.pop("email", None)
    return render_template('log_out.html')

@auth.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        # Check if username already exists
        existing_user = User.query.filter_by(username=username, email=email).first()
        if existing_user:
            # Store username and email in session
            session['username'] = existing_user.username
            session['email'] = existing_user.email
            return redirect(url_for('auth.user'))
        
        password = request.form.get('password')
        # Add validation and user creation logic here
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', category='success')
        # Store username and email in session
        session['username'] = username
        session['email'] = email
        return redirect(url_for('auth.user'))
    
    return render_template('sign_up.html')

@auth.route('/mypage')
def user():
    # Retrieve username and email from session
    username = session.get('username')
    email = session.get('email')
    # Render user template
    return render_template('user.html', username=username, email=email)