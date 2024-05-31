# models.py
from website.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False, default='')
    
    def __init__(self, username, email, password, description):
        self.username = username
        self.email = email
        self.password = password
        self.description = description 
    
    def get_id(self):
        return str(self.id)