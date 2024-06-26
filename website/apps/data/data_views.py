from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.database import db
from datetime import datetime
from website.apps.share_models import Game, User, UserGame
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
        query = query.lower()
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

@data.route('/game', methods=["POST", "GET"])
def game():
    username = session.get('username')
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        flash('User not found!', category='error')
        return redirect(url_for('auth.login'))
    if request.method == "GET":
        game_name = request.args.get('game')
        game = Game.query.filter_by(title=game_name).first()
        user = session['username']
        user = User.query.filter_by(username=user).first()
        existing_association = UserGame.query.filter_by(user_id=user.user_id, game_id=game.game_id).first()
        user_owned_games = user.owned_games
        boolean_value = False
        if existing_association is not None:
            boolean_value = existing_association.completion
    return render_template('game2.html', game=game, user=user, existing_association=existing_association, user_owned_games=user_owned_games, boolean_value=boolean_value)
