from trainee import db, login_manager, app # goes into init.py and pulls db
from flask_login import UserMixin # add required attributes and methods for loading user
from itsdangerous import URLSafeTimedSerializer as Serializer
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 3 column table for the user login database
# made it this far https://youtu.be/71EU8gnZqZQ?si=BoYsLeX3yzLg_ZVl&t=876
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpeg')
    password = db.Column(db.String(80), nullable=False)

    # creates a relationship between posts and Session
    posts = db.relationship('Session', backref='author', lazy=True) 

    # TODO:figure out itsdangrous and python 3.11 compatability issue
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod #says we're not expecting the self argument
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self): # how our object is printed when we print User object
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(50), nullable = False)
    # date = db.Column(db.DateTime, nullable = False)
    # time = db.Column(db.DateTime, nullable = False)
    # date_posted = db.Column(db.DateTime, nullable=False, default='datetime.utcnow')
    skillFocus = db.Column(db.String(200), nullable=False, default='No Preferance')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): 
        return f"Session('{self.title}', '{self.location}', '{self.skillFocus}')"