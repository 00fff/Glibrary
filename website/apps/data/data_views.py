from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.database import db
from datetime import datetime
from website.apps.share_models import Game, User
import requests
from website.apps.igdb import get_game, top_games
data = Blueprint('data', __name__, template_folder='templates/data')
from website.apps.cache_config import cache


CLIENT_ID = 'w69saddrm609bdexx1qv7k8334kspc'
CLIENT_SECRET = 'raegpu6z9tovkh7j92mch8mk7uf31t'

@data.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        query = request.form.get('query')
        existing_game = Game.query.filter_by(title=query).first()
        if existing_game:
            game_info = {
                "name": existing_game.title,
                "summary": existing_game.description,
                "platforms": existing_game.platform.split(', '),
                "first_release_date": existing_game.release_date,
                "genres": existing_game.genre.split(', '),
                "involved_companies": existing_game.developer.split(', '),
                "rating": existing_game.rating,
                "cover": existing_game.art,
            }
            return render_template('search.html', game_info=[game_info])
        else:
            game_info = get_game(query)
            if game_info:
                return render_template('search.html', game_info=game_info)
            else:
                error_message = f"No results found for '{query}'."
                return render_template('search.html', error_message=error_message)
    else:
        return render_template('search.html')
    
def game():
    if 'username' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if user not logged in
    username = session['username']
    if request.method == "POST":
        game_name = request.form.get('game_name')
        if game_name:
            add_game = get_game(game_name)
            title = add_game.get('name')
            description = add_game.get('summary')
            art = add_game.get('summary')
            platform = add_game.get('platform')
            genre = add_game.get('genre')
            release_date = add_game.get('release_date')
            developer = add_game.get('developer')
            publisher = add_game.get('publisher')
            rating = add_game.get('rating')

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
