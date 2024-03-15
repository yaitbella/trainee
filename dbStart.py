# short script to start db
# Note: this needs to be run before running the application
from trainee import create_app, db
from trainee.config import Config

app = create_app(Config)

with app.app_context():
    db.create_all()