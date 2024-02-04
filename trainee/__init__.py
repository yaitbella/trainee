from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from trainee.config import Config


db = SQLAlchemy() #creates database instance
bcrypt = Bcrypt()
login_manager = LoginManager() # allows our app + flask to work together
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info" 

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import blueprint objects here and register them with our route
    from trainee.users.routes import users
    from trainee.sessions.routes import sessions
    from trainee.main.routes import main
    from trainee.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(sessions)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    from .models import User, Session

    with app.app_context():
        db.create_all()
        
    return app
