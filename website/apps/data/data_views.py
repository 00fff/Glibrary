from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.database import db
from datetime import datetime
from website.apps.share_models import Game, User
import requests
from website.apps.igdb import get_game, top_games

data = Blueprint('data', __name__, template_folder='templates/data')

CLIENT_ID = 'w69saddrm609bdexx1qv7k8334kspc'
CLIENT_SECRET = 'raegpu6z9tovkh7j92mch8mk7uf31t'

@data.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        # Handle the POST request
        query = request.form.get('query')  # Ensure this matches the form field name
        game_info = get_game(query)
        print(game_info)
        if game_info:
            return render_template('search.html', game_info=game_info)
        else:
            error_message = f"No results found for '{query}'."
            return render_template('search.html', error_message=error_message)
    else:
        # Handle the GET request
        return render_template('search.html')

@data.route('/game', methods=["POST", "GET"])
def game():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if user not logged in
    username = session['username']
    if request.method == "POST":
        # Retrieve game details from the form
        title = request.form.get('title')
        description = request.form.get('description')
        art = request.form.get('art')
        platform = request.form.get('platform')
        genre = request.form.get('genre')
        release_date_str = request.form.get('release_date')  # Get the date string from the form

        # Convert the date string to a Python date object
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()

        developer = request.form.get('developer')
        publisher = request.form.get('publisher')
        rating = request.form.get('rating')

        # Create a new Game object
        new_game = Game(title=title, description=description, art=art, platform=platform, genre=genre, 
                        release_date=release_date, developer=developer, publisher=publisher, 
                        rating=rating)

        # Retrieve the current user
        username = session['username']
        user = User.query.filter_by(username=username).first()

        # Append the new game to the user's owned games
        user.owned_games.append(new_game)

        # Commit changes to the database
        db.session.add(new_game)
        db.session.commit()

        # Redirect to a success page or another appropriate page
        return redirect(url_for('views.home'))

    return render_template('game.html')
