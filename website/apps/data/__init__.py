from flask import Blueprint
games = Blueprint('games', __name__, template_folder='templates/games')
from . import game_views