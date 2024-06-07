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

@data.route('/game', methods=["POST", "GET"])
def game():
    if request.method == "GET":
        game = request.form.get('game')
        
    return render_template('game.html')

