from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, TimeField, SelectField

class SessionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    skillFocus = StringField('Skill Focus', validators=[DataRequired()])
    skillFocus = SelectField(u'Session Skill Focus', validators=[DataRequired()], choices=[('', ''),
                                                                                           ('Shooting', 'Shooting'), 
                                                                                            ('Passing', 'Passing'), 
                                                                                            ('Dribbling', 'Dribbling'),
                                                                                            ('Defending', 'Defending'), 
                                                                                            ('Fitness', 'Fitness'),
                                                                                            ('Strength', 'Strength')])
    session_date = DateField('Session Date', format='%Y-%m-%d', validators=[DataRequired()])
    session_time = TimeField('Session Time', validators=[DataRequired()])
    submit = SubmitField('Post Session')