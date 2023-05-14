#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def viewHomePage():
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


@app.route('/search')
def searchPets():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='true', port=5000)
