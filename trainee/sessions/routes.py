from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from flask_login import login_required, current_user

from trainee import db
from trainee.models import Session
from trainee.sessions.forms import SessionForm

sessions=Blueprint('sessions', __name__)

@sessions.route('/session/new', methods=['GET','POST'])
@login_required
def new_session():
    form = SessionForm()
    if form.validate_on_submit():
        sesh = Session(title=form.title.data, 
                        location=form.location.data,
                        user_id = current_user.id,
                        skillFocus = form.skillFocus.data,
                        session_date=form.session_date.data, 
                        session_time=form.session_time.data,
                        session_host=current_user.username)
        
        db.session.add(sesh)
        db.session.commit()
        flash('your session has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_session.html',
                           title='New Session', 
                           form=form, 
                           legend='New Session')

@sessions.route("/session/<int:session_id>")
def session(session_id):
    session = Session.query.get_or_404(session_id)
    return render_template('session.html', 
                           title=session.title, 
                           session=session)

# TODO: seems like this sometimes doesn't work
@sessions.route("/session/<int:session_id>/update", methods=['GET','POST'])
@login_required
def update_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session.session_host != current_user.username:
        abort(403)
    form = SessionForm()
    if form.validate_on_submit():
        session.title = form.title.data
        session.location = form.location.data
        db.session.commit()
        flash('your session has been updated!', 'success')
        return redirect(url_for('sessions.session', session_id=session.id))
    elif request.method == 'GET':
        form.title.data = session.title
        form.location.data = session.location
    return render_template('new_session.html', 
                           title='Update Session', 
                           form=form, 
                           legend='Update Session')

# TODO: figure out boostrap MODAL delete button 
@sessions.route("/session/<int:session_id>/delete", methods=['POST'])
@login_required
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session.author != current_user:
        abort(403)
    db.session.delete(session)
    db.session.commit()
    flash('Your session has been deleted!', 'success')
    return redirect(url_for('main.home'))

@sessions.route("/session/<int:session_id>/join", methods=['POST'])
def join_session(session_id):
    session = Session.query.get_or_404(session_id)
    if current_user in session.participants:
        flash('You have already joined the session!', 'warning')
    else:
        session.particpants.append(current_user)
    db.session.commit()
    flash('You have joined the session!', 'success')
    return redirect(url_for('sessions.session', session_id=session.id))