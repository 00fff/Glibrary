from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from werkzeug.utils import secure_filename
from website.database import db
import os 

auth = Blueprint('auth', __name__, template_folder='templates/auth')
# Set the upload folder and allowed extensions for the profile pictures
UPLOAD_FOLDER = 'path/to/upload/folder'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
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
            # If user already exists, redirect to user page
            session['username'] = existing_user.username
            session['email'] = existing_user.email
            return redirect(url_for('auth.user'))
        
        password = request.form.get('password')
        description = request.form.get('description')
        # Check if the profile picture is provided in the request
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '':
                # Check if the file extension is allowed
                if profile_picture.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                    # Secure the filename and save the file to the upload folder
                    filename = secure_filename(profile_picture.filename)
                    profile_picture.save(os.path.join(UPLOAD_FOLDER, filename))
                    flash('Profile picture uploaded successfully!', category='success')
                else:
                    flash('Invalid file format!', category='error')
            else:
                flash('No file selected!', category='error')

        # Add validation and user creation logic here
        new_user = User(username=username, email=email, password=password, description=description)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', category='success')
        
        # Store username and email in session
        session['username'] = username
        session['email'] = email
        
        return redirect(url_for('auth.user'))
    
    return render_template('sign_up.html')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@auth.route('/mypage')
def user():
    # Retrieve username and email from session
    username = session.get('username')
    email = session.get('email')
    # Render user template
    return render_template('user.html', username=username, email=email)


@auth.route('/edit', methods=["POST", "GET"])
def edit():
    username = session.get('username')
    existing_user = User.query.filter_by(username=username).first()
    current_password = existing_user.password
    print(current_password)
    print(f'this is the current username{username}')
    if request.method == 'POST':
        same_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        new_username = request.form.get('username')
        print(f'this is the new username{new_username}')
        new_email = request.form.get('email')
        new_description = request.form.get('description')
        print(same_password)

        if current_password != same_password:
            flash('Incorrect current password!', category='error')
            return redirect(url_for('auth.edit'))

        if new_username:
            # Check if the new username already exists
            if new_username != username and User.query.filter_by(username=new_username).first():
                flash('Username already exists!', category='error')
                return redirect(url_for('auth.edit'))
            
            existing_user.username = new_username
            # print(f'current exitings username{existing_user.username}')
            session['username'] = new_username
            # print(f'session username{session['username']}')
        if new_email:
            existing_user.email = new_email
            session['email'] = new_email
        
        if new_description:
            existing_user.description = new_description
            session['description'] = new_description
        if new_password:
            existing_user.description = new_description
            session['description'] = new_description
       # Update the profile picture if provided
        """if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(UPLOAD_FOLDER, filename))
            existing_user.profile_picture = filename"""

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('auth.user'))

    return render_template('edit_home.html', user=existing_user)
