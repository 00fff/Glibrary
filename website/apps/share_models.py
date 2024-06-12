# models.py
from website.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'  # Explicitly set the table name to 'user'
    
    user_id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Unique username, cannot be null
    email = db.Column(db.String(150), unique=True, nullable=False)  # Unique email, cannot be null
    password = db.Column(db.String(150), nullable=False)  # Password, cannot be null
    description = db.Column(db.String(150), nullable=False, default='')  # Description with a default empty string
    
    # Use UserGame for the relationship to include the completion status
    owned_games = db.relationship('UserGame', back_populates='user')  # Relationship to UserGame, back_populates links to UserGame.user

    def __init__(self, username, email, password, description):
        self.username = username
        self.email = email
        self.password = password
        self.description = description 
    
    def get_id(self):
        return str(self.user_id)  # Return user_id as a string

class Game(db.Model):
    __tablename__ = 'game'  # Explicitly set the table name to 'game'
    
    game_id = db.Column(db.Integer, primary_key=True)  # Primary key for the game
    title = db.Column(db.String(150), unique=True, nullable=False)  # Unique title, cannot be null
    description = db.Column(db.String(150), nullable=False)  # Description, cannot be null
    art = db.Column(db.String(150), nullable=False)  # Art URL or path, cannot be null
    platform = db.Column(db.String(50), nullable=False)  # Platform, cannot be null
    genre = db.Column(db.String(50), nullable=False)  # Genre, cannot be null
    release_date = db.Column(db.Date)  # Release date, optional
    developer = db.Column(db.String(100))  # Developer, optional
    publisher = db.Column(db.String(100))  # Publisher, optional
    rating = db.Column(db.String(10))  # Rating, optional
    
    # Use UserGame for the relationship to include the completion status
    owners = db.relationship('UserGame', back_populates='game')  # Relationship to UserGame, back_populates links to UserGame.game

    def __init__(self, title, description, art, platform, genre, release_date=None, developer=None, publisher=None, rating=None):
        self.title = title
        self.description = description
        self.art = art
        self.platform = platform
        self.genre = genre
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher
        self.rating = rating

class UserGame(db.Model):
    __tablename__ = 'user_game_association'  # Explicitly set the table name to 'user_game_association'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)  # Foreign key referencing user.user_id, part of the composite primary key
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), primary_key=True)  # Foreign key referencing game.game_id, part of the composite primary key
    completion = db.Column(db.Boolean, default=False)  # Completion status for the game for each user, default is False
    
    user = db.relationship('User', back_populates='owned_games')  # Relationship back to User, linking to owned_games in User
    game = db.relationship('Game', back_populates='owners')  # Relationship back to Game, linking to owners in Game
