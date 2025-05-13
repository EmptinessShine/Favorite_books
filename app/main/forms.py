from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from config import Config

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=140)])
    author = StringField('Author', validators=[DataRequired(), Length(max=140)])
    genre = StringField('Genre', validators=[Optional(), Length(max=100)])
    publication_year = IntegerField('Publication Year', validators=[Optional(), NumberRange(min=-4000, max=2100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=5000)])
    cover_image = FileField('Cover Image', validators=[
        Optional(),
        FileAllowed(Config.ALLOWED_EXTENSIONS, 'Images only!')
    ])
    submit = SubmitField('Save Book')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')