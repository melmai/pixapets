#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from petfinder import get_pets, get_pet, get_breeds
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

import routes, models

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='true', port=5000)
