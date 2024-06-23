from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from website.apps.share_models import User, Game, UserGame, FriendModel
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from website.database import db
from flask_mail import Message
from website.apps.mail import mail
import os
import hashlib
from website.utils.utils import send_email
home_email = "00fffprojects@gmail.com"
auth = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='static')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join('static', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
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
            return redirect(url_for('auth.user', username=session['username']))
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
        pfp = request.files['profile_picture']
        print(pfp)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', category='error')
            return redirect(url_for('auth.sign_up'))
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        if pfp and allowed_file(pfp.filename):
            filename = secure_filename(pfp.filename)
            unique_filename = f"{username}_{filename}"
            save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            pfp.save(save_path)
            profile_image = unique_filename
        else:
            profile_image = "blank_pfp.png"

        hashed_password = hash_password_sha256(password)
        new_user = User(username=username, email=email, password=hashed_password, description=description, profile_image=profile_image)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', category='success')
        welcome_html = render_template('wemail.html', username=new_user.username)
        send_email("Welcome To GameLibraries!", email, "Thank you for registering an account for GameLibraries, Have fun Gaming!", welcome_html)
        session['username'] = username
        session['email'] = email
        
        return redirect(url_for('auth.user', username=session['username']))
    
    return render_template('sign_up.html')


@auth.route('/<username>', methods=["POST", "GET"])
def user(username):
    current_user = User.query.filter_by(username=session['username']).first()
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
        
        
        
# Ensure game_completion is interpreted as boolean True or False
        game_completion = request.form.get("game_completion")
        if game_completion == "True":
            game_completion = True
        else:
            game_completion = False

        game_title = request.form.get("game_boolean")
        game = Game.query.filter_by(title=game_title).first()

        if game:
            boolean_association = UserGame.query.filter_by(user=user, game=game).first()
            
            if boolean_association:
                # Update completion status based on the checkbox value
                boolean_association.completion = game_completion
                db.session.commit()
                flash("Game completion status updated.")
            else:
                flash("Game not found in user library.")
        else:
            flash("Could Not Find Game")


    # Refetch the user's games from the database
    user_owned_games = UserGame.query.filter_by(user=user).all()
    completed_games = []
    if user_owned_games is not None:
        for game in user_owned_games:
            if game.completion:
                completed_games.append(game)
        completed_games_count = len(completed_games)


    return render_template('user.html', username=username, email=email, user=user, user_owned_games=user_owned_games, completed_games_count=completed_games_count, current_user=current_user)



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
        new_pfp = request.files.get('new_profile_picture')
        # new_pfp = request.form.get('profile_picture')

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

        # Update username if provided
        if new_pfp:
            existing_user.profile_image = new_pfp
            session['profile_image'] = new_pfp

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('auth.user', username=session['username']))

    return render_template('edit_home.html', user=existing_user)

@auth.route('/friends', methods=["POST", "GET"])
def friends():
    if 'username' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('auth.login'))

    current_user = User.query.filter_by(username=session['username']).first()
    
    if current_user is None:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))
    
    if request.method == "POST":
        #adding friend
        remove_friend = request.form.get('remove_user_name')
        friend_name = request.form.get('added_user_name')
        if friend_name:
            friend = User.query.filter_by(username=friend_name).first()
            cuser_id = current_user.user_id
            friend_id = friend.user_id
            print(cuser_id, friend_id)
            check_friendship = FriendModel.query.filter_by(user_id=cuser_id, friend_id=friend_id).first()
            check_friendship2 =FriendModel.query.filter_by(user_id=friend_id, friend_id=cuser_id).first()
            if check_friendship or check_friendship2:
                flash("User Already In Your Friend's List")
                return render_template('friends.html', current_user=current_user)
            else:
                new_friendship = FriendModel(user_id=cuser_id, friend_id=friend_id)
                db.session.add(new_friendship)
                db.session.commit()
            return render_template('friends.html', current_user=current_user)
        if remove_friend:
            remove_friend = User.query.filter_by(username=remove_friend).first()
            cuser_id = current_user.user_id
            friend_id = remove_friend.user_id
            remove_friendship = FriendModel.query.filter_by(user_id=cuser_id, friend_id=friend_id).first()
            remove_friendship2 =FriendModel.query.filter_by(user_id=friend_id, friend_id=cuser_id).first()
            if remove_friendship:
                db.session.delete(remove_friendship)
                db.session.commit()
            elif remove_friendship2:
                db.session.delete(remove_friendship2)
                db.session.commit()
            return render_template('friends.html', current_user=current_user)
    return render_template('friends.html', current_user=current_user)

@auth.route('/notification', methods=["POST", "GET"])
def notification():
    if 'username' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('auth.login'))
    current_user = User.query.filter_by(username=session['username']).first()
    return render_template('notification.html', current_user=current_user)

@auth.route('/friend-search', methods=["POST", "GET"])
def friend_search():
    if 'username' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('auth.login'))

    current_user = User.query.filter_by(username=session['username']).first()
    found_names = None

    if request.method == "POST":
        query = request.form.get('query')
        if query:
            found_names = User.query.filter(User.username.contains(query)).all()
            if not found_names:
                flash("No users found.", "warning")
        else:
            flash("Please enter a search term.", "warning")

    return render_template('friendsearch.html', current_user=current_user, found_names=found_names)

@auth.route('/delete', methods=["POST", "GET"])
def delete_user():
    if 'username' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('auth.login'))
    current_user = User.query.filter_by(username=session['username']).first()
    db.session.delete(current_user)
    db.session.commit()
    session.pop('username', None)
    session.pop('email', None)
    return render_template('delete.html')