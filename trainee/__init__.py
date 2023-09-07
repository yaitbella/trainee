import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #connects appflie to datebase
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app) #creates database instance
bcrypt = Bcrypt(app)

login_manager = LoginManager(app) # allows our app + flask to work together
login_manager.login_view = 'login'
login_manager.login_message_category = "info" 

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
# login_manager.init_app(app) 

# @login_manager.user_loader # used to reload the user object from the user ID stored in the session
# def load_user(user_id):
#     return User.query.get(int(user_id))

from trainee import routes #this is at bottom to avoid circular imports with "app"