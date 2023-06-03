from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo, ValidationError, Optional

class SignUp(FlaskForm):
    # first_name - string
    first_name = StringField('First Name', validators=[DataRequired()])

    # last_name - string
    last_name = StringField('Last Name', validators=[DataRequired()])

    # email - email
    email = EmailField('Email', validators=[DataRequired(), Email()])

    # zipcode - integer
    location = StringField('Zip Code', validators=[DataRequired(), Length(min=5, max=5)])

    # password, confirm_password - password
    # TODO: Make sure passwords match
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    # pet_type - select
    pet_type = SelectField('Pet Type', choices=[('all', 'All'), ('dog', 'Dog'), ('cat', 'Cat')], validators=[Optional()])
    
    # breed - select
    breed = SelectField('Breed', choices=[('all', 'All Breeds')], validators=[Optional()])
    
    # age - select
    age = SelectField('Age', choices=[('all', 'All Ages'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    
    # distance - integer
    distance = SelectField('Distance', choices=[('10', '10 Miles'), ('25', '25 Miles'), ('50', '50 Miles'), ('100', '100 Miles'), ('250', '250 Miles')], validators=[Optional()], default='100')

    register_bttn = SubmitField("Sign Up")