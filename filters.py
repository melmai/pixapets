from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Optional


class PetFilter(FlaskForm):
    """Form for filtering pets"""
    pet_type = SelectField('Pet Type', choices=[('dogs', 'Dogs'), ('cats', 'Cats')])
    location = StringField("Location", render_kw={"placeholder": "Location"})
    distance = SelectField('Distance', choices=[('10', '10 Miles'), ('25', '25 Miles'), ('50', '50 Miles'), ('100', '100 Miles'), ('250', '250 Miles')], validators=[Optional()], default='100')
    breed = SelectField('Breed', choices=[], validators=[Optional()], render_kw={"placeholder": "Type"})
    age = SelectField('Age', choices=[('all', 'All Ages'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])
    search_bttn = SubmitField("Search")