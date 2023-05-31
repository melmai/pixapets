#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask, render_template
from petfinder import get_pets, get_pet
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


def create_connection():
    conn = sqlite3.connect(app.config['users.spbpro'])
    return conn

def create_user_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id integer primary key autoincrement, username text unique not null, password text not null)''')
    conn.commit()
    conn.close()

@app.route('/login', methods =['GET', 'POST'])
def login():
    return render_template('login.html', login=Login())


@app.route('/profile')
def viewProfile():
    return render_template('profile.html')


@app.route('/pets/<string:pet_type>')
def searchPets(pet_type):
    pets = get_pets(pet_type)
    print(pets)
    return render_template('pets.html', pet_type=pet_type, pets=pets, filter=PetFilter())

@app.route('/pet/<int:pet_id>')
def viewPetDetails(pet_id):
    pet = get_pet(pet_id)
    print(pet)
    return render_template('details.html', pet_id=pet_id, pet=pet)

if __name__ == '__main__':
    app.config['users.spbpro'] = 'db/users.spbpro'

    create_user_table()
    app.run(host='0.0.0.0', debug='true', port=5000)
