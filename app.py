#!/usr/bin/python3
# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from petfinder import get_pets
from filters import PetFilter
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/willi/OneDrive/Desktop/pixapets/db/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

app.secret_key="secret"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

     

class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    favorites = db.Column(db.String, nullable = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()  # Create an instance of the RegistrationForm

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            msg = 'Username already exists. Please go back'
            return render_template('register.html', msg=msg)

        new_user = User(username=username, password=password)
        db.session.add(new_user)  # Add the new user to the session
        db.session.commit()  # Commit the changes to the database

        return 'Registration successful!'

    return render_template('register.html', form=form)
    # if request.method == 'GET':
    #     return render_template('register.html')

    # if request.method =='POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     existing_user = User.query.filter_by(username = username).first()
    #     if existing_user:
    #         msg = 'Username already exists. Please go back'
    #         return render_template('register.html', msg = msg)
        
        # new_user=User(username=username, password = password)
        # db.session.add(new_user)
        # db.session.commit()
        # msg = 'Registration successful!'
        # return render_template('register.html', msg = msg)


def create_connection():
    conn = sqlite3.connect(app.config['users'])
    return conn

def create_user_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id integer primary key autoincrement, username varchar unique not null, password varchar not null, preferences text, favorites text )''')
    conn.commit()
    conn.close()

@app.route('/login', methods =['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        existing_user = User.query.filter(User.username == username).first()
        print(f"Existing user: {existing_user}")

        if existing_user:
            print(f"Existing user password: {existing_user.password}")
            if existing_user.password == password:
                return 'Login Successful'
            else:
                return 'Oops invalid password!'
        else:
            return 'Oops! Invalid username :('

    return render_template('login.html')
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']

    #     existing_user = User.query.filter_by(username=username).first()
    #     if existing_user:
    #         if existing_user.password == password:
    #             return 'Login Successful'
    #         else:
    #             return 'Oops invalid password!'
    #     else:
    #         return 'Oops! Invalid username :('
    
    # return render_template('login.html')







    #So i am confusion
    #     conn = create_connection()
    #     cursor = conn.cursor()
    #     cursor.execute('select * from users where username =?', (username,))
    #     user = cursor.fetchone()
    #     conn.close()
    #     if user and user[2] == password:
    #         return 'Login Successful'
    #     else:
    #         return 'Oops! Invalid username or password :('  
    # return render_template('login.html')


@app.route('/profile')
def viewProfile():
    return render_template('profile.html')


@app.route('/pets/<string:pet_type>')
def searchPets(pet_type):
    pets = get_pets(pet_type)
    print(pets)
    return render_template('pets.html', pet_type=pet_type, pets=pets, filter=PetFilter())


if __name__ == '__main__':
    with app.app_context():
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()
        app.config['users'] = 'C:/Users/willi/OneDrive/Desktop/pixapets/db/users.db'
        create_user_table()
    app.run(host='0.0.0.0', debug='true', port=5000)
