from flask import (render_template, url_for, redirect, 
                   flash, request, Blueprint)
from flask_login import (login_user, login_required, 
                         logout_user, current_user)

from trainee import db, bcrypt
from trainee.models import User, Session, Player
from trainee.users.forms import (RegisterForm, LoginForm, UpdateAccountForm, 
                           RequestResetForm, ResetPasswordForm)
from trainee.users.utils import save_picture, send_reset_email

users=Blueprint('users', __name__)

# Route for user login
@users.route("/login", methods=['GET', 'POST']) 
def login():
    # redirect to home page is user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm() # Create an instance of the login form

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # find the user by their email in databse
        
        # succesful login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in the user and set the 'remember me' option if provided
            login_user(user, remember=form.remember.data)
            
            # Get the next page URL from the 'next' query parameter if it exists, else redirect to home page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # If login is unsuccessful, show a flash message
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    # Print form validation errors (for debugging purposes)
    print(form.errors)
    
    # Render the login template with the login form
    return render_template('login.html', title='Login', form=form)


@users.route("/register", methods=['GET', 'POST']) 
def register():
    if current_user.is_authenticated: # redirect to home page if user already logged in
        return redirect(url_for('main.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #adds user to database
        user =  User(username=form.username.data,
                      email=form.email.data,
                        password=hashed_password)
        db.session.add(user)
        db.session.commit() 

        # Create a corresponding Player object and associate it with the user
        player = Player(player_user=user)  # Assuming 'user' is the relationship in the Player model (see models.py)
        db.session.add(player)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@users.route("/user/<string:username>") # this is where you land; runs home() function
def user_sessions(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    sessions=Session.query.filter(Session.author.contains(user)).paginate(page=page, per_page=5) #TODO: Session.query.order_by(Session.date_posted.desc())
    return render_template('user_sessions.html', sessions=sessions, user=user) #this goes into /templates and looks for "home.html"


# page that will ask user for email to request resetting password
@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

#where they actually reset the password
@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit() 
        flash(f'Password has been updated for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
