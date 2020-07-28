from flask import Blueprint
from flask import render_template
from flask import request

# import different db models for querying
from flaskblog.models import Post
from flaskblog import db

# create a main blueprint
main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    # get number of page from URL query ?page=x
    page = request.args.get("page", 1, type=int)
    # paginate posts, so they don't load all at once
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
