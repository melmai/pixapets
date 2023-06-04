from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass 

class SignUpForm(FlaskForm):
    """Form for signing up"""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    location = StringField('Zip Code', validators=[DataRequired(), Length(min=5, max=5)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    pet_type = SelectField('Pet Type', choices=[('all', 'All'), ('dog', 'Dog'), ('cat', 'Cat')], validators=[Optional()])
    breed = NonValidatingSelectField('Breed', choices=[('all', 'All Breeds')], validators=[Optional()])
    age = SelectField('Age', choices=[('all', 'All Ages'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    distance = SelectField('Distance', choices=[('10', '10 Miles'), ('25', '25 Miles'), ('50', '50 Miles'), ('100', '100 Miles'), ('250', '250 Miles')], validators=[Optional()], default='100')
    register_bttn = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    """Form for logging in"""
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    signin_bttn = SubmitField('Sign In')

class EditProfileForm(SignUpForm):
    """Form for editing profile"""
    update_bttn = SubmitField("Update Profile")