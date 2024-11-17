# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    content = TextAreaField('Post Content', validators=[DataRequired()])
