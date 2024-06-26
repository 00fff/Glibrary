# website/apps/share_models.py

from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
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
    
    # Define friendships and user_friends relationships correctly
    friendships = db.relationship('FriendModel', foreign_keys='FriendModel.user_id', back_populates='user_rel', cascade='all, delete-orphan', viewonly=True)
    user_friends = db.relationship('FriendModel', foreign_keys='FriendModel.friend_id', back_populates='friend_rel', cascade='all, delete-orphan', viewonly=True)

    def __init__(self, username, email, password, description='', profile_image=None):
        self.username = username
        self.email = email
        self.password = password
        self.description = description
        self.profile_image = profile_image  # Initialize the profile image

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            user_id = data.get('user_id')
        except (TypeError, ValueError):
            print("type")
            return None
        return User.query.get(user_id)


class FriendModel(db.Model):
    __tablename__ = 'user_to_user_association'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    
    # Define user and friend relationships with correct back_populates
    user_rel = db.relationship('User', foreign_keys=[user_id], back_populates='friendships')
    friend_rel = db.relationship('User', foreign_keys=[friend_id], back_populates='user_friends')

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id






class Game(db.Model):
    __tablename__ = 'game'

    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))  # Adjust the length as per your requirements
    description = db.Column(db.Text)
    art = db.Column(db.String)
    platform = db.Column(db.String)
    genre = db.Column(db.String)
    release_date = db.Column(db.Date)
    developer = db.Column(db.String(150))  # Increase the length as per your needs
    publisher = db.Column(db.String(150))  # Increase the length as per your needs
    rating = db.Column(db.Integer)
    
    owners = db.relationship('UserGame', back_populates='game')

    def __init__(self, title, description, art, platform, genre, release_date=None, developer=None, publisher=None, rating=None):
        self.title = title[:255]  # Ensure truncation to fit within the new length if needed
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