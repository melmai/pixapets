from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User Model for storing user related details"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    
class FavoritePet(db.Model):
    """Favorite Pet Model for storing favorite pets"""
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Favorite('{self.pet_id}', '{self.user_id}')"
    
class Preferences(db.Model):
    """Preferences Model for storing user preferences"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pet_type = db.Column(db.String(20), nullable=True)
    distance = db.Column(db.Integer, nullable=True)
    breed = db.Column(db.String(120), nullable=True)
    age = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Preferences('{self.user_id}', '{self.pet_type}', '{self.location}', '{self.distance}', '{self.breed}', '{self.age}')"