import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
db = SQLAlchemy()  # sqlite db object
bcrypt = Bcrypt()  # to hash user's password
login_manager = LoginManager()  # login manager to manage user sessions
# to tell our extension where to redirect when accessing restricted pages
login_manager.login_view = "users.login"  # function name of our route
login_manager.login_message_category = "info"  # replicate flash msg but for login
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    # register blueprints to our app
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # create db if not exists
    with app.app_context():
        db.create_all()

    return app
