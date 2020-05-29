from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request

# import flask db object, bcrypt obj for hashing pwd
from flaskblog import db, bcrypt

# import different forms
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.users.forms import RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email

# import different db models for querying
from flaskblog.models import User, Post

# flask_login to manage user sessions
from flask_login import login_user, current_user, logout_user, login_required


# create a user blueprint
users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    # if current user is already logged in, they should not be able to access register page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    # otherwise send them to registration page
    form = RegistrationForm()  # create reg form object
    if form.validate_on_submit():  # validate data based on conditions specified in form
        # generate pwd hash, to be stored in db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)  # add user to db
        db.session.commit()  # commit changes
        flash("Your account has been created! You are now able to log in", "success")
        # after successfully registration, redirect user to login page
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    # if current user is already logged in, they should not be able to access login page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # match hash of password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # after logging in, redirect to restricted page that user was trying to access, without login
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # if pic uploaded
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file  # update image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account Info Updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":  # to fill existing user details
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for("static", filename=f"profile_pics/{current_user.img_file}")
    return render_template(
        "account.html", title="Account", img_file=img_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    # get number of page from URL query ?page=x
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # paginate posts, so they don't load all at once
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
