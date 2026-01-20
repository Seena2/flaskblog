import os
import secrets
from PIL import Image
from flask import url_for, current_app as app
from flask_mail import Message
from flaskblog import mail

# function to save profile picture
def save_picture(form_picture):
    # save the uploaded picture to the filesystem
    # generate random hex for picture filename, to avoid name conflicts using secrets module
    random_hex = secrets.token_hex(8)
    # get the file extension of the uploaded picture, 
    # note "_" is used to ignore the first value(filename) returned by os.path.splitext
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # path to save the picture starting from the app root directory
    picture_path = os.path.join(app.root_path, 'static/profilePics', picture_fn)
    # resize the image before saving using Pillow
    output_size = (125, 125)
    i = Image.open(form_picture) #create Pillow image object
    i.thumbnail(output_size)#Resize image
    # save the resized image to the filesystem
    i.save(picture_path)
    return picture_fn




# function sending reset email
def sendResetEmail(user):
    # get token for the user using the get_reset_token method defined in User model  
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@seenadev.com', recipients=[user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

