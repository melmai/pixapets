#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from petfinder import get_pets, get_pet, get_breeds
from filters import PetFilter
from signup import SignUp
from login import Login
from flask_sqlalchemy import SQLAlchemy
from database import db


# Create a new Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixapets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init database
with app.app_context():
    db.init_app(app)
    from models import User, FavoritePet, Preferences
    db.create_all()
    db.session.commit()

# routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():

    form = SignUp()
    if request.method == 'POST':

        # if fields are valid, create user
        if form.validate_on_submit():
            # create user object
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data) 

            # set optional values for user
            if form.location.data:
                new_user.location = form.location.data

            # add user to database
            db.session.add(new_user)

            try:
                db.session.commit()
            except:
                db.session.rollback()

            # get user ID
            user = User.query.filter_by(email=form.email.data).first()

            # create null preferences and set optional values
            new_preferences = Preferences(user_id=user.id)
            if form.pet_type.data:
                new_preferences.pet_type = form.pet_type.data
            if form.distance.data:
                new_preferences.distance = form.distance.data
            if form.breed.data:
                new_preferences.breed = form.breed.data
            if form.age.data:
                new_preferences.age = form.age.data
            
            # add preferences to database
            db.session.add(new_preferences)
            
            # commit changes
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return render_template('register.html', signup=SignUp(), errors=form.errors)
            
            flash('Thanks for registering!')
            return redirect(url_for('home'))
        else:
            if form.email.errors:
                for error in form.email.errors:
                    flash(error)
            return render_template('register.html', signup=SignUp())


    return render_template('register.html', signup=SignUp())

@app.route('/breeds/<string:pet_type>')
def get_breeds_by_type(pet_type):
    return jsonify(get_breeds(pet_type))

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
    # if os.path.exists('pixapets.db'):
    #     os.remove('pixapets.db')

    # with app.app_context():
    #     db.create_all()

    app.run(host='0.0.0.0', debug='true', port=5000)

