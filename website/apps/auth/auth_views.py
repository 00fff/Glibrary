from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from website.apps.share_models import User, Game, UserGame
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from website.database import db
from flask_mail import Message
from website.apps.mail import mail
import os
import hashlib

auth = Blueprint('auth', __name__, template_folder='templates/auth')




UPLOAD_FOLDER = 'path/to/upload/folder'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def hash_password_sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def welcome_email(username, sender, recipients):
    msg = Message(subject=f"Welcome To GameLibrary, {username}", sender={sender}, recipients=[recipients])
    msg.body = "Have Fun Gathering Your favorite games"
    mail.send(msg)


@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower()
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user and existing_user.password == hash_password_sha256(password):
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
        email = request.form.get('email').lower()  # Convert email to lowercase
        password = request.form.get('password')
        description = request.form.get('description')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', category='error')
            return redirect(url_for('auth.sign_up'))
        
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '' and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('Profile picture uploaded successfully!', category='success')
            else:
                flash('Invalid file format!', category='error')

        hashed_password = hash_password_sha256(password)
        new_user = User(username=username, email=email, password=hashed_password, description=description)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', category='success')
        session['username'] = username
        session['email'] = email
        
        return redirect(url_for('auth.user'))
    
    return render_template('sign_up.html')


@auth.route('/mypage', methods=["POST", "GET"])
def user():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    email = session.get('email').lower()  # Convert session email to lowercase

    if request.method == 'POST':
        # Handle adding a game
        game_title = request.form.get("game_name")
        game = Game.query.filter_by(title=game_title).first()
        
        if game is not None:  # Ensure the game exists
            check_game = UserGame.query.filter_by(user=user, game=game).first()
            if check_game:
                flash("Game Already in Game Library")
            else:
                new_game = UserGame(user=user, game=game)  # Create UserGame object with instances
                db.session.add(new_game)  # Add new_game to the session
                db.session.commit()  # Commit the session to insert the new record into the database
                flash("Game Added Successfully")
        else:
            flash("Game not found")
        # Handle removing a game
        remove_game_title = request.form.get("game_remove")
        remove_game = Game.query.filter_by(title=remove_game_title).first()
        
        if remove_game is not None:  # Ensure the game exists
            existing_association = UserGame.query.filter_by(user=user, game=remove_game).first()
            if existing_association:
                db.session.delete(existing_association)  # Delete the existing association from the session
                db.session.commit()  # Commit the session to delete the record from the database
                flash("Game removed from your library.")
            else:
                flash("Game not in library")
        else:
            flash("Game to remove not found")

    # Refetch the user's games from the database
    user_owned_games = UserGame.query.filter_by(user=user).all()
    
    return render_template('user.html', username=username, email=email, user=user, user_owned_games=user_owned_games)



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
        new_email = request.form.get('email').lower()  # Convert new email to lowercase
        new_description = request.form.get('description')

        # Check if the current password is correct
        if existing_user.password != hash_password_sha256(current_password):
            flash('Incorrect current password!', category='error')
            return redirect(url_for('auth.edit'))

        # Check if the new username already exists (if it is different from the current username)
        if new_username and new_username != username and User.query.filter_by(username=new_username).first():
            flash('Username already exists!', category='error')
            return redirect(url_for('auth.edit'))

        # Update username if provided
        if new_username:
            existing_user.username = new_username
            session['username'] = new_username

        # Update email if provided
        if new_email:
            existing_user.email = new_email
            session['email'] = new_email

        # Update description if provided
        if new_description:
            existing_user.description = new_description

        # Update password if provided
        if new_password:
            hashed_new_password = hash_password_sha256(new_password)
            existing_user.password = hashed_new_password

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('auth.user'))

    return render_template('edit_home.html', user=existing_user)