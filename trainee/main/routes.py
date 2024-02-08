from flask import render_template, request, Blueprint
from flask_login import current_user
from trainee.models import Session

main=Blueprint('main', __name__)

@main.route("/")
@main.route("/home") # this is where you land; runs home() function
def home():
    page = request.args.get('page', 1, type=int)
    sessions=Session.query.paginate(page=page, per_page=5) #TODO: Session.query.order_by(Session.date_posted.desc())
    return render_template('home.html', sessions=sessions, user=current_user) #this goes into /templates and looks for "home.html"


