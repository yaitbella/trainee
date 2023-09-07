from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from trainee.models import User
from flask_login import current_user

class RegisterForm(FlaskForm): #inherits from flask form
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"}) # string field that must be field out; 4 - 20 characters

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Submit')
        
    def validate_username(self, username): #method that verifies if there already exists a username or not
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('Someone has that username. Be more creative bro')

    def validate_email(self, email): #method that verifies if there already exists an email or not
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('Email is already taken mate')
                
class LoginForm(FlaskForm): #inherits from flask form
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm): #inherits from flask form
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"}) # string field that must be field out; 4 - 20 characters
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')
        
    def validate_username(self, username): #method that verifies if there already exists a username or not
        if username.data != current_user.username:
            existing_user_username = User.query.filter_by(username=username.data).first()
            if existing_user_username:
                raise ValidationError('Someone has that username. Be more creative bro')

    def validate_email(self, email): #method that verifies if there already exists an email or not
        if email.data != current_user.email:
            existing_user_email = User.query.filter_by(email=email.data).first()
            if existing_user_email:
                raise ValidationError('Email is already taken mate')
            
class SessionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = TextAreaField('location', validators=[DataRequired()])
    submit = SubmitField('Post Session')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email): #method that verifies if there already exists an email or not
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email is None:
            raise ValidationError('Account with associated email not found')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()] )
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Reset Password')