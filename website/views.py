from flask import Blueprint, render_template, flash
from flask_login import login_required
from website.apps.igdb import top_games
views = Blueprint('views', __name__)
@views.route('/')
def home():
    games = top_games()
    if games is None:
        flash('Error retrieving game data.', 'error')
        games = []
    return render_template('home.html', games=games)