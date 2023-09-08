import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from trainee import mail

def save_picture(form_picture):
    #generates unique filename for profile picture
    random_hex = secrets.token_hex(8) 
    _, f_ext = os.path.splitext(form_picture.filename) 
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    
    # block that resizes the uploaded image
    output_size = (125, 125)
    resizedImg = Image.open(form_picture)
    resizedImg.thumbnail(output_size)
    resizedImg.save(picture_path)

    return picture_filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='train.ee.webapp@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, please ignore this email
'''
    mail.send(msg)