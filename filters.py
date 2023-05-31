from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional


class PetFilter(FlaskForm):

    # type - select
    type = SelectField('Type', choices=[('all', 'Type (All)'), ('dog', 'Dog'), ('cat', 'Cat')], validators=[Optional()])

    # location - text
    location = StringField("Location", render_kw={"placeholder": "Location"})

    # breed - select
    breed = SelectField('Breed', choices=[('all', 'Breeds (All)')], validators=[Optional()], render_kw={"placeholder": "Type"})

    # age - select
    age = SelectField('Age', choices=[('all', 'Age (All)'), ('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[Optional()])

    # submit - button
    search_bttn = SubmitField("Search")