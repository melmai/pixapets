from app import app, login_manager
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from petfinder import get_pets, get_pet, get_breeds
from filters import PetFilter
from forms import SignUpForm, LoginForm, EditProfileForm
from database import db
from models import User, FavoritePet, Preferences
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():

    form = SignUpForm()
    if request.method == 'POST':

        # if fields are valid, create user
        if form.validate_on_submit():
            # create user object
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data) 
            new_user.set_password(form.password.data)

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
                return render_template('register.html', signup=form, errors=form.errors)
            
            flash('Thanks for registering!')
            return redirect(url_for('home'))
        else:
            if form.email.errors:
                for error in form.email.errors:
                    flash(error)
            return render_template('register.html', signup=form)


    return render_template('register.html', signup=form)


@app.route('/breeds/<string:pet_type>')
def get_breeds_by_type(pet_type):
    return jsonify(get_breeds(pet_type))


@app.route('/dashboard/<int:user_id>')
@login_required
def dashboard(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('dashboard.html', filter=PetFilter(), user=user)

@login_manager.user_loader
def load_user(user_id):    
    return User.query.get(int(user_id))


@app.route('/login', methods =['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f"Welcome, ${user.first_name}!")
                return redirect(url_for('dashboard', user_id=user.id))

    return render_template('login.html', login=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.unauthorized_handler
def unauthorized():
  return "Sorry you must be logged in to view this page"

@app.route('/edit_profile')
@login_required
def edit_profile():
    return render_template('edit_profile.html', edit=EditProfileForm())


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
