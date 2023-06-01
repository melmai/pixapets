#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run
from flask import Flask, render_template, request, redirect, url_for, session, flash
from petfinder import get_pets, get_pet, get_breeds
from filters import PetFilter
from signup import SignUp
from login import Login
from flask_sqlalchemy import SQLAlchemy

# Create a new Flask application instance
app = Flask(__name__)
app.secret_key="secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database instance
db = SQLAlchemy(app)

# database configuration
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

# routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():

    form = SignUp()
    form.breed.choices = get_breeds(form.pet_type.data)
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('register.html', signup=form)
        else:
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data) 
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()

            flash('Thanks for registering!')
            return redirect(url_for('home'))

    return render_template('register.html', signup=SignUp())

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    return render_template('login.html', login=Login())


@app.route('/profile')
def viewProfile():
    return render_template('profile.html')


@app.route('/pets/<string:pet_type>', methods=['GET', 'POST'])
def search_pets(pet_type):
    breeds = get_breeds(pet_type)
    filter = PetFilter()
    filter.breed.choices = filter.breed.choices + breeds

    if request.method == 'POST':
        breed = filter.breed.data.lower()
        pets = get_pets(pet_type, location=filter.location.data, distance=filter.distance.data, breed=breed, age=filter.age.data)
        print(pets)
    else:
        pets = get_pets(pet_type)
        
    return render_template('pets.html', pet_type=pet_type, pets=pets, filter=filter)


@app.route('/pet/<int:pet_id>')
def viewPetDetails(pet_id):
    pet = get_pet(pet_id)
    print(pet)
    return render_template('details.html', pet_id=pet_id, pet=pet)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='true', port=5000)
