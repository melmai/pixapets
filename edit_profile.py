from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional

# TODO: Could be refactored since shares most fields with the sign up form
class Edit_Profile(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

    email = EmailField('Email', validators=[Email()])

    zipcode = IntegerField('Zip Code', validators=[Length(min=5, max=5)])

    # TODO: Make sure passwords match
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo(password, message='Passwords must match')])


    pet_type = SelectField('Pet Type', choices=[('None', ''), ('all', 'All'), ('dog', 'Dog'), ('cat', 'Cat')], validators=[Optional()])
    
    # TODO: Generate list of breeds from API
    breed = SelectField('Breed', choices=[('None', ''), ('all', 'All'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    
    age = SelectField('Age', choices=[('None', ''), ('all', 'All'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    
    # TODO: Make this make sense
    distance = StringField("Distance", validators=[Optional()])


    update_bttn = SubmitField("Update Profile")