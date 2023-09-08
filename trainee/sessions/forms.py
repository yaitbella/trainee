from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SessionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = TextAreaField('location', validators=[DataRequired()])
    submit = SubmitField('Post Session')