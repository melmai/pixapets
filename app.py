#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask, render_template
from petfinder import get_pets, get_pet

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/profile')
def viewProfile():
    return render_template('profile.html')


@app.route('/pets/<string:pet_type>')
def searchPets(pet_type):
    pets = get_pets(pet_type)
    print(pets[0])
    return render_template('pets.html', pet_type=pet_type, pets=pets)

@app.route('/pets/<string:pet_type>/<int:pet_id>')
def viewPetDetails(pet_type, pet_id):
    pet = get_pet(pet_id)
    print(pet)
    return render_template('details.html', pet_type=pet_type, pet_id=pet_id, pet=pet)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='true', port=5000)
