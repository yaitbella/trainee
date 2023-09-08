from trainee import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# new SQLAlchmy to create db files // NOTE: YOU HAVE TO RUN THESE BEFORE DOING ANYTHING WITH DB
# from trainee import app, db
# app.app_context().push()
# db.create_all()