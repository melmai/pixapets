from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    
class FavoritePet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Favorite('{self.pet_id}', '{self.user_id}')"
    
class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pet_type = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Preferences('{self.user_id}', '{self.pet_type}', '{self.location}', '{self.distance}', '{self.breed}', '{self.age}')"