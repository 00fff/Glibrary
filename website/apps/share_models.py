# models.py

from website.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False, default='')
    profile_image = db.Column(db.String(150), nullable=True) 
    
    owned_games = db.relationship('UserGame', back_populates='user', cascade='all, delete-orphan')
    friendships = db.relationship('FriendModel', foreign_keys='FriendModel.user_id', backref=db.backref('friendships'), cascade='all, delete-orphan')
    user_friends = db.relationship('FriendModel', foreign_keys='FriendModel.friend_id', backref=db.backref('user_friendships'), cascade='all, delete-orphan')

    def __init__(self, username, email, password, description='', profile_image=None):
        self.username = username
        self.email = email
        self.password = password
        self.description = description
        self.profile_image = profile_image  # Initialize the profile image



class FriendModel(db.Model):
    __tablename__ = 'user_to_user_association'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='user')
    friend = db.relationship('User', foreign_keys=[friend_id], backref='friend')

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id



class Game(db.Model):
    __tablename__ = 'game'
    
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
    
    owners = db.relationship('UserGame', back_populates='game')

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

    def __init__(self, user, game):
        self.user = user
        self.game = game