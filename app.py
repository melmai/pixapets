#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask, render_template, request, redirect, url_for, session, flash
from petfinder import get_pets, get_pet, get_breeds
from filters import PetFilter
from signup import SignUp
from login import Login

app = Flask(__name__)
app.secret_key="secret"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('register.html', signup=SignUp())
  

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
