# models.py
from website.database import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False, default='')
    owned_games = db.relationship('Game', secondary='user_game_association', back_populates='owners')
    def __init__(self, username, email, password, description):
        self.username = username
        self.email = email
        self.password = password
        self.description = description 
    
    def get_id(self):
        return str(self.user_id)  # Fixed to use user_id instead of id

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    art = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date)
    developer = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    rating = db.Column(db.String(10))
    owners = db.relationship('User', secondary='user_game_association', back_populates='owned_games')


    # Add more attributes as needed

    def __init__(self, title, description, art, platform, genre, release_date=None, developer=None, publisher=None, rating=None, price=None, playtime=None):
        self.title = title
        self.description = description
        self.art = art
        self.platform = platform
        self.genre = genre
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher
        self.rating = rating



user_game_association = db.Table('user_game_association',
    db.Column('game_id', db.Integer, db.ForeignKey('game.game_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
)

