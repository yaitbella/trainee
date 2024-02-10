from flask import (render_template, url_for, redirect, 
                   flash, request, Blueprint)
from flask_login import (login_user, login_required, 
                         logout_user, current_user)

from trainee import db, bcrypt

from trainee.models import User, Session, Player

from trainee.users.forms import (RegisterForm, LoginForm, UpdateAccountForm, 
                           RequestResetForm, ResetPasswordForm)

from trainee.players.forms import PlayerForm
from trainee.users.utils import save_picture, send_reset_email

players=Blueprint('players', __name__) # creates 'players' Blueprint

@players.route("/player", methods=['GET', 'POST'])
@login_required
def player_page():
    form = PlayerForm()

    if form.validate_on_submit():    
        current_user.position = form.position.data
        current_user.strongFoot = form.strongFoot.data
        db.session.commit()
        flash('your player details have been updated! You better not have lied ;)', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.position.data = current_user.position
        form.strongFoot.data = current_user.strongFoot
        #test test test
    return render_template('player.html', title='Player', form=form)
