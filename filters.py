from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# class LoginForm(FlaskForm):
#     email = EmailField('email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
#     password = PasswordField('password', validators=[DataRequired(), Length(min=5, max=50)])
#     my_textfield = StringField("TextLabel")
#     my_submit = SubmitField("SubmitName")

class PetFilter(FlaskForm):
    # type - select
    type = SelectField('Type', choices=[('dog', 'Dog'), ('cat', 'Cat')])

    # location - text
    location = StringField("Location")

    # breed - select
    breed = SelectField('Breed', choices=[('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')])

    # age - select
    age = SelectField('Age', choices=[('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')])

    # submit - button
    search_bttn = SubmitField("Search")