from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort

# flask_login to manage user sessions
from flask_login import current_user, login_required

# import flask db object
from flaskblog import db

# import different db models for querying
from flaskblog.models import Post

# import different forms
from flaskblog.posts.forms import PostForm


# create a post blueprint
posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":  # populate with existing info
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
