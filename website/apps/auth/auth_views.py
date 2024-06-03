from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.apps.share_models import User
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from website.database import db
import os

auth = Blueprint('auth', __name__, template_folder='templates/auth')

UPLOAD_FOLDER = 'path/to/upload/folder'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and check_password_hash(existing_user.password, password):
            flash("Logged in", category="success")
            session['username'] = existing_user.username
            session['email'] = existing_user.email
            return redirect(url_for('auth.user'))
        else:
            flash('Invalid email or password!', category='error')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop("username", None)
    session.pop("email", None)
    return render_template('log_out.html')

@auth.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', category='error')
            return redirect(url_for('auth.sign_up'))

        password = request.form.get('password')
        description = request.form.get('description')
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '' and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('Profile picture uploaded successfully!', category='success')
            else:
                flash('Invalid file format!', category='error')

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, email=email, password=hashed_password, description=description)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', category='success')
        
        session['username'] = username
        session['email'] = email
        
        return redirect(url_for('auth.user'))
    
    return render_template('sign_up.html')

@auth.route('/mypage')
def user():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    email = session.get('email')
    return render_template('user.html', username=username, email=email, user=user)

@auth.route('/edit', methods=["POST", "GET"])
def edit():
    username = session.get('username')
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        flash('User not found!', category='error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_description = request.form.get('description')

        if not check_password_hash(existing_user.password, current_password):
            flash('Incorrect current password!', category='error')
            return redirect(url_for('auth.edit'))

        if new_username and new_username != username and User.query.filter_by(username=new_username).first():
            flash('Username already exists!', category='error')
            return redirect(url_for('auth.edit'))

        if new_username:
            existing_user.username = new_username
            session['username'] = new_username
        
        if new_email:
            existing_user.email = new_email
            session['email'] = new_email
        
        if new_description:
            existing_user.description = new_description
        
        if new_password:
            hashed_new_password = generate_password_hash(new_password, method="pbkdf2:sha256")
            existing_user.password = hashed_new_password

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('auth.user'))

    return render_template('edit_home.html', user=existing_user)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
