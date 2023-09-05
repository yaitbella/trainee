from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email, EqualTo

class RegisterForm(FlaskForm): #inherits from flask form
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"}) # string field that must be field out; 4 - 20 characters

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    # def validate_username(self, username): #method that verifies if there already exists a username or not
    #     existing_user_username = User.query.filter_by(username=username.data).first()
    #     if existing_user_username:
    #         raise ValidationError('That username already exists. Please choose a different one.')
        
class LoginForm(FlaskForm): #inherits from flask form
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"}) # string field that must be field out; 4 - 20 characters

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')
