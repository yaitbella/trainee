from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, TimeField

class PlayerForm(FlaskForm):
    position = StringField('Position', validators=[DataRequired()])
    strongFoot = StringField('Dominant Foot', validators=[DataRequired()])