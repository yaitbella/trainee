# RESOURCE: venv- https://www.youtube.com/watch?v=31WU0Dhw4sk
from trainee import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


    
# to hard erase the database after making schema changes:
# from trainee import create_app, db
# from trainee.config import Config
# app = create_app(Config)

# with app.app_context():
#     db.create_all()
# or
# with app.app_context():
#     db.drop_all()
    
# --- VENV ---
    # source venv/bin/activate


# TODO: 
    # fix delete session button
    # fix profile picture routing problem
    # add only 30 minute increments for session Times
    # add ability to LEAVE a session after joining
    # figure out itsdangrous and python 3.11 compatability issue
    # custom flash message in complete_sessions for players stats who cannot be updated
    # ---
    # DONE: notification when you have already joined a session
    # DONE: reorder home page so newest session are at top