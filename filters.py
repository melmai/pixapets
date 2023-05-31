from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional


class PetFilter(FlaskForm):
    # location - text
    location = StringField("Location", render_kw={"placeholder": "Location"})

    # distance - select
    distance = SelectField('Distance', choices=[('10', '10 Miles'), ('25', '25 Miles'), ('50', '50 Miles'), ('100', '100 Miles'), ('250', '250 Miles')], validators=[Optional()], default='100')

    # breed - select
    breed = SelectField('Breed', choices=[], validators=[Optional()], render_kw={"placeholder": "Type"})

    # age - select
    age = SelectField('Age', choices=[('all', 'All Ages'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])

    # submit - button
    search_bttn = SubmitField("Search")