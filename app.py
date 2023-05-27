#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from petfinder import get_pets
from filters import PetFilter

app = Flask(__name__)
app.secret_key="secret"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('insert into users (username, password) values(?,?)', (username, password))
        return redirect(url_for('login'))

    return render_template('register.html')


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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('select * from users where username =?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and user[2] == password:
            return 'Login Successful'
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/profile')
def viewProfile():
    return render_template('profile.html')


@app.route('/pets/<string:pet_type>')
def searchPets(pet_type):
    pets = get_pets(pet_type)
    print(pets)
    return render_template('pets.html', pet_type=pet_type, pets=pets, filter=PetFilter())


if __name__ == '__main__':
    app.config['users.spbpro'] = 'db/users.spbpro'

    create_user_table()
    app.run(host='0.0.0.0', debug='true', port=5000)
