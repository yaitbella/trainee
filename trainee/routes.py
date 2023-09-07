import secrets
import os
from PIL import Image

from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import (login_user, login_required, LoginManager, 
                         logout_user, current_user)
from flask_mail import Message
from trainee.forms import (RegisterForm, LoginForm, UpdateAccountForm, 
                           SessionForm, RequestResetForm, ResetPasswordForm)
from datetime import datetime
from trainee.models import User, Session
from trainee import app, db, bcrypt, mail

# from datetime import datetime

@app.route("/")
@app.route("/home") # this is where you land; runs home() function
def home():
    page = request.args.get('page', 1, type=int)
    sessions=Session.query.paginate(page=page, per_page=5) #TODO: Session.query.order_by(Session.date_posted.desc())
    return render_template('home.html', sessions=sessions) #this goes into /templates and looks for "home.html"

@app.route("/login", methods=['GET', 'POST']) 
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    print(form.errors)
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST']) 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #adds user to database
        user =  User(username=form.username.data,
                      email=form.email.data,
                        password=hashed_password)
        db.session.add(user)
        db.session.commit() 

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    #generates unique filename for profile picture
    random_hex = secrets.token_hex(8) 
    _, f_ext = os.path.splitext(form_picture.filename) 
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    
    # block that resizes the uploaded image
    output_size = (125, 125)
    resizedImg = Image.open(form_picture)
    resizedImg.thumbnail(output_size)
    resizedImg.save(picture_path)

    return picture_filename

@app.route("/profile", methods=['GET', 'POST'])
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
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route('/session/new', methods=['GET','POST'])
@login_required
def new_session():
    form = SessionForm()
    if form.validate_on_submit():
        sesh = Session(title=form.title.data, 
                        location=form.location.data, #TODO:
                        user_id = current_user.id)
        db.session.add(sesh)
        db.session.commit()
        flash('your session has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_session.html',
                           title='New Session', 
                           form=form, 
                           legend='New Session')

@app.route("/session/<int:session_id>")
def session(session_id):
    session = Session.query.get_or_404(session_id)
    return render_template('session.html', 
                           title=session.title, 
                           session=session)

@app.route("/session/<int:session_id>/update", methods=['GET','POST'])
@login_required
def update_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session.author != current_user:
        abort(403)
    form = SessionForm()
    if form.validate_on_submit():
        session.title = form.title.data
        session.location = form.location.data
        db.session.commit()
        flash('your session has been updated!', 'success')
        return redirect(url_for('session', session_id=session.id))
    elif request.method == 'GET':
        form.title.data = session.title
        form.location.data = session.location
    return render_template('new_session.html', 
                           title='Update Session', 
                           form=form, 
                           legend='Update Session')

# TODO: figure out boostrap MODAL delete button 
@app.route("/session/<int:session_id>/delete", methods=['POST'])
@login_required
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session.author != current_user:
        abort(403)
    db.session.delete(session)
    db.session.commit()
    flash('Your session has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>") # this is where you land; runs home() function
def user_sessions(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    sessions=Session.query.filter_by(author=user).paginate(page=page, per_page=5) #TODO: Session.query.order_by(Session.date_posted.desc())
    return render_template('user_sessions.html', sessions=sessions, user=user) #this goes into /templates and looks for "home.html"

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='train.ee.webapp@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, please ignore this email
'''
    mail.send(msg)

# page that will ask user for email to request resetting password
@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

#where they actually reset the password
@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit() 
        flash(f'Password has been updated for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
