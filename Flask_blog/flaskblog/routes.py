from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort

# import flask object, db object, bcrypt obj for hashing pwd
from flaskblog import app, db, bcrypt

# import different forms
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm

# import different db models for querying
from flaskblog.models import User, Post

# flask_login to manage user sessions
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image  # modifying profile image
import secrets
import os

db.create_all()

# Dummy data, when it was under development and not connected to sqlite db
# posts = [
#     {
#         "author": "Manav",
#         "title": "Blog Post 1",
#         "content": "First post content",
#         "date_posted": "May 19, 2020",
#     },
#     {
#         "author": "Jane Doe",
#         "title": "Blog Post 2",
#         "content": "Second post content",
#         "date_posted": "May 21, 2020",
#     },
# ]


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    # if current user is already logged in, they should not be able to access register page
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # if current user is already logged in, they should not be able to access login page
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # match hash of password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    """Save picture
    :form_picture - image data"""
    # create a random hex, to rename file to so it may not collide
    random_hex = secrets.token_hex(8)
    # get file name and extension of uploaded file
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext  # create new path to save img file
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)  # set the dimension of image to save
    i = Image.open(form_picture)  # open image
    i.thumbnail(output_size)  # resize image
    i.save(picture_path)  # save image

    # delete current profile pic from db
    curr_img = os.path.join(app.root_path, "static/profile_pics", current_user.img_file)
    os.remove(curr_img)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("account"))
    elif request.method == "GET":  # to fill existing user details
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for("static", filename=f"profile_pics/{current_user.img_file}")
    return render_template(
        "account.html", title="Account", img_file=img_file, form=form
    )


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your Post Created!", "success")
        return redirect(url_for("home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # if current user is not author of post, abort with invalid request
    if post.author != current_user:
        abort(403)
    form = PostForm()  # create new form obj
    # if form is validated, update information
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated Successfully", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":  # populate with existing info
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))

