from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, LoginManager, logout_user, current_user
from flask_bcrypt import Bcrypt

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #connects appflie to datebase
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app) #creates database instance

# with app.app_context(): #needed to add this to create tables? still not working
#     db.create_all()

bcrypt = Bcrypt(app)

login_manager = LoginManager() # allows our app + flask to work together
login_manager.init_app(app) 
login_manager.login_view = "login"

@login_manager.user_loader # used to reload the user object from the user ID stored in the session
def load_user(user_id):
    return User.query.get(int(user_id))

# 3 column table for the user login database
# made it this far https://youtu.be/71EU8gnZqZQ?si=BoYsLeX3yzLg_ZVl&t=876
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@app.route("/") # this is where you land; runs home() function
def home():
    return render_template('home.html') #this goes into /templates and looks for "home.html"

@app.route("/login", methods=['GET', 'POST']) 
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', title='login', form=form)


@app.route("/register", methods=['GET', 'POST']) 
def register():
    form = RegisterForm()

    if form.validate_on_submit(): # stores the hashed version of the password on submission
        flash(f'Account Created for {form.username.data}!', 'success')
        # hashed_password = bcrypt.generate_password_hash(form.password.data)
        # new_user = User(username=form.username.data, password=hashed_password)
        # db.session.add(new_user)
        # db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard(): 
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/session/new', methods=['GET','POST'])
@login_required
def new_session():
    return render_template('new_session.html')

if __name__ == '__main__':
    app.run(debug=True)

# # A player user
# class Player:
#     def __init__(self, name, age, location):
#         self.name = name
#         self.age = age
#         self.location = location

# # A session is the training session that a user can create to be shared with others
# class Session:
#     def __init__(self, name, date, time, location, focus):
#         self.name = name
#         self.date = date
#         self.time = time
#         self.location = location
#         self.focus = focus