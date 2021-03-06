import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app
from flask_mail import Message
from flaskblog import mail
from flask_login import current_user


def save_picture(form_picture):
    """Save picture
    :form_picture - image data"""
    # create a random hex, to rename file to so it may not collide
    random_hex = secrets.token_hex(8)
    # get file name and extension of uploaded file
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext  # create new path to save img file
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )

    output_size = (125, 125)  # set the dimension of image to save
    i = Image.open(form_picture)  # open image
    i.thumbnail(output_size)  # resize image
    i.save(picture_path)  # save image

    # delete current profile pic from db
    if "default" not in current_user.img_file:
        curr_img = os.path.join(
            current_app.root_path, "static/profile_pics", current_user.img_file
        )
        os.remove(curr_img)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
