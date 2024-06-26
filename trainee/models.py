#           ---     RESOURCES + DOCUMENTATION   ---             #
# declaring models doc: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# many to many relationships sqlAlchemy: https://www.youtube.com/watch?v=47i-jzrrIGQ
#                                        https://www.youtube.com/watch?v=IlkVu_LWGys

from trainee import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

# allows Flask-Login to load user objects from database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# asssociation table that creates Many To Many relationship between User and Session model
user_session_table = db.Table('user_session_table', 
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
                     db.Column('session_id', db.Integer, db.ForeignKey('session.id')))

# model to store all user account and profile information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpeg')
    password = db.Column(db.String(80), nullable=False)

    # to accesss Session object through a User object, use ___.sessions
    sessions = db.relationship('Session', secondary=user_session_table, backref='author', lazy=True) 

    # to access Player object through a User object, use 'UserObj'.user_player
    user_player = db.relationship('Player', backref='user', lazy=True, uselist=False)

    # method that retrieves the token used to reset the password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod # <-says we're not expecting the self argument
    # method that verifies reset token
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    # defines how our object is printed when we print a User object
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(50), nullable = False)
    session_date = db.Column(db.Date, nullable = False)
    session_time = db.Column(db.Time, nullable = False)
    skillFocus = db.Column(db.String(200), nullable=False, default='No Preferance')
    session_host = db.Column(db.Integer, nullable=False)
    # date_posted = db.Column(db.DateTime, nullable=False, default='datetime.utcnow')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participants = db.relationship('User', secondary=user_session_table, backref='joined_sessions', lazy=True)
    
    # defines how our object is printed when we print a Session object
    def __repr__(self): 
        return f"Session('{self.title}', '{self.location}', '{self.skillFocus}')"
    
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable = True, default='Bench Player')
    strong_foot = db.Column(db.String(50), nullable = True, default='No Preferance')
    pace = db.Column(db.Integer[0,100], nullable=True, default=50)
    shooting = db.Column(db.Integer[0,100], nullable=True, default=50)
    passing = db.Column(db.Integer[0,100], nullable=True, default=50)
    dribbling = db.Column(db.Integer[0,100], nullable=True, default=50)
    defending = db.Column(db.Integer[0,100], nullable=True, default=50)
    physicality = db.Column(db.Integer[0,100], nullable=True, default=50)

    # to access User object through a Player object, use PlayerName.player_user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_user = db.relationship('User', backref='player', lazy=True) 

    # defines how our object is printed when we print a Player object
    def __repr__(self): 
        return f"Player('{self.position}', '{self.strong_foot}', '{self.pace}')"