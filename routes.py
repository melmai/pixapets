from app import app, login_manager
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from petfinder import get_pets, get_pet, get_breeds
from filters import PetFilter
from forms import SignUpForm, LoginForm, EditProfileForm
from database import db
from models import User, FavoritePet, Preferences
from flask_login import login_user, current_user, logout_user, login_required


# publicly available routes
@app.route('/')
def home():
    """Return the home page."""
    # get dogs and cats with photos
    dogs = get_pets('dog', number=20)
    dogs_with_photos = [dog for dog in dogs if dog['primary_photo_cropped']]
    dogs_with_photos = dogs_with_photos[:4]

    cats = get_pets('cat', number=20)
    cats_with_photos = [cat for cat in cats if cat['primary_photo_cropped']]
    cats_with_photos = cats_with_photos[:4]

    # get favorites if user is logged in
    if current_user.is_authenticated:
        favorites = FavoritePet.query.filter_by(user_id=current_user.id).all()
        return render_template('home.html', dogs=dogs_with_photos, cats=cats_with_photos, favorites=favorites)
    
    return render_template('home.html', dogs=dogs_with_photos, cats=cats_with_photos, favorites=[])


@app.route('/pets/<string:pet_type>', methods=['GET', 'POST'])
def search_pets(pet_type):
    """Return a list of pets for a given pet type."""
    # get breeds for pet type
    breeds = get_breeds(pet_type)
    filter = PetFilter()
    filter.breed.choices = filter.breed.choices + breeds

    # if form is submitted, get pets with filters
    if request.method == 'POST':
        breed = filter.breed.data.lower()
        pets = get_pets(pet_type, location=filter.location.data, distance=filter.distance.data, breed=breed, age=filter.age.data)
    else:
        pets = get_pets(pet_type)

    # if user is logged in, get favorites
    if current_user.is_authenticated:
        favorite_pets = FavoritePet.query.filter_by(user_id=current_user.id).all()
        favorite_ids = [pet.pet_id for pet in favorite_pets]
        return render_template('pets.html', pet_type=pet_type, pets=pets, filter=filter, favorite_ids=favorite_ids)
        
    return render_template('pets.html', pet_type=pet_type, pets=pets, filter=filter, favorite_ids=[])


@app.route('/pet/<int:pet_id>')
def view_pet_details(pet_id):
    """Return details for a given pet."""
    # get pet details
    pet = get_pet(pet_id)

    # if user is logged in, check if pet is a favorite
    if current_user.is_authenticated:
        is_favorite = FavoritePet.query.filter_by(pet_id=pet_id, user_id=current_user.id).first()
        return render_template('details.html', pet_id=pet_id, pet=pet, is_favorite=is_favorite)
    
    return render_template('details.html', pet_id=pet_id, pet=pet, is_favorite=False)


@app.route('/breeds/<string:pet_type>')
def get_breeds_by_type(pet_type):
    """Return a list of breeds for a given pet type."""
    return jsonify(get_breeds(pet_type))


# Database routes
@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Register a new user."""
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
        
        # if form is not valid, flash error
        else:
            if form.email.errors:
                for error in form.email.errors:
                    flash(error)
            return render_template('register.html', signup=form)

    return render_template('register.html', signup=form)


@app.route('/dashboard/<int:user_id>')
@login_required
def dashboard(user_id):
    """Return a user's dashboard."""
    # get user and favorites
    user = User.query.filter_by(id=user_id).first_or_404()
    favorites_by_id = FavoritePet.query.filter_by(user_id=user_id).all()
    breeds = get_breeds("dog")
    filter = PetFilter()
    filter.breed.choices = filter.breed.choices + breeds

    # get pet details for each favorite
    favorites = []
    for favorite in favorites_by_id:
        pet = get_pet(favorite.pet_id)

        # if pet is found, add it to favorites
        if pet != "pet not found":
            favorites.append(pet)
        else:
            # remove pet from favorites
            db.session.delete(favorite)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return "Tried to remove but failed"
            
    return render_template('dashboard.html', filter=filter, user=user, favorites=favorites)


@login_manager.user_loader
def load_user(user_id):    
    """Return a user object given a user ID."""
    return User.query.get(int(user_id))


@app.route('/login', methods =['GET', 'POST'])
def login():
    """Log a user in."""
    form = LoginForm()

    # if form is submitted and valid, try to log user in
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            # if user exists and password is correct, log user in
            if user and user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                return redirect(next or url_for('dashboard', user_id=user.id))
            # if user does not exist or password is incorrect, flash error
            else:
                flash('Invalid username or password')
                return render_template('login.html', login=form)
            
        # if form is not valid, flash error
        else:
            if form.email.errors:
                for error in form.email.errors:
                    flash(error)
            return render_template('login.html', login=form)

    return render_template('login.html', login=form)


@app.route("/logout")
@login_required
def logout():
    """Log a user out."""
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized():
  """Redirect unauthorized users to login page."""
  flash("Sorry you must be logged in to view this page")
  return redirect(url_for('login'))

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    """Edit a user's profile."""
    # get user and preferences
    user = User.query.filter_by(id=user_id).first()
    preferences = Preferences.query.filter_by(user_id=user_id).first()
    form = EditProfileForm(obj=user)

    if request.method == 'POST':
        if form.validate_on_submit():
            # update user and preferences
            user.set_password(form.password.data)
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.location = form.location.data
            preferences.pet_type = form.pet_type.data
            preferences.distance = form.distance.data
            preferences.breed = form.breed.data
            preferences.age = form.age.data

            # commit changes
            try:
                db.session.commit()
                flash('Profile updated successfully!')
            except:
                db.session.rollback()
                flash('Error updating profile')

        # if form is not valid, flash error
        else:
            if form.email.errors:
                for error in form.email.errors:
                    flash(error)
            return render_template('edit_profile.html', edit=form, user_id=user.id)

    return render_template('edit_profile.html', edit=form, user_id=user.id)


@app.route('/favorite/<int:pet_id>/<int:user_id>')
def update_favorite(pet_id, user_id):
    """Update a user's favorites."""
    # check if pet is already a favorite
    favorite = FavoritePet.query.filter_by(pet_id=pet_id, user_id=user_id).first()

    # if pet is a favorite, remove it
    if favorite:
        db.session.delete(favorite)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "Tried to remove but failed"
        return jsonify("Removed")
    # if pet is not a favorite, add it
    else:
        return add_favorite(pet_id, user_id)


def add_favorite(pet_id, user_id):
    """Add a pet to a user's favorites."""
    # create new favorite
    new_favorite = FavoritePet(pet_id=pet_id, user_id=user_id)

    # add favorite to database and commit change
    db.session.add(new_favorite)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify("Tried to add but failed")
    
    return jsonify("Added to favorites")