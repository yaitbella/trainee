# file used to completely erase and refresh the database
# Note: DO NOT USE UNLESS PLANNING TO ERASE EVERYTHING
from trainee import create_app, db
from trainee.config import Config
app = create_app(Config)


with app.app_context():
    db.drop_all()
    
with app.app_context():
    db.create_all()