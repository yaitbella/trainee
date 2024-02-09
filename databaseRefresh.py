from trainee import create_app, db
from trainee.config import Config
app = create_app(Config)


with app.app_context():
    db.drop_all()
    
with app.app_context():
    db.create_all()