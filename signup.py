from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional

class SignUp(FlaskForm):
    # first_name - string
    first_name = StringField('First Name')

    # last_name - string
    last_name = StringField('Last Name')

    # email - email
    email = EmailField('Email')

    # zipcode - integer
    zipcode = IntegerField('Zip Code')

    # password, confirm_password - password
    # TODO: Make sure passwords match
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')

    # pet_type - select
    pet_type = SelectField('Pet Type', choices=[('None', ''), ('all', 'All'), ('dog', 'Dog'), ('cat', 'Cat')], validators=[Optional()])
    
    # breed - select
    # TODO: Generate list of breeds from API
    breed = SelectField('Breed', choices=[('None', ''), ('all', 'All'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    
    # age - select
    age = SelectField('Age', choices=[('None', ''), ('all', 'All'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    
    # TODO: Make this make sense
    distance = StringField("Distance", validators=[Optional()])


    register_bttn = SubmitField("Sign Up")