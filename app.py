#!/usr/bin/python3

# This command will run the app on localhost:5000 and will allow you to see the refreshed app in your browser
# flask --app app.py --debug run

from flask import Flask
from database import db
from flask_login import LoginManager


# Create a new Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixapets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init database
with app.app_context():
    db.init_app(app)
    import models
    db.create_all()
    db.session.commit()

# create login manager
login_manager = LoginManager()
login_manager.init_app(app)

import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='true', port=5000)
