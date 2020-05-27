import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

# secret key for protection against modifying cookies, forgery attaacks etc.
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"  # sqlite db path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # suppresses deprecation warning
db = SQLAlchemy(app)  # sqlite db object
bcrypt = Bcrypt(app)  # to hash user's password
login_manager = LoginManager(app)  # login manager to manage user sessions
# to tell our extension where to redirect when accessing restricted pages
login_manager.login_view = "login"  # function name of our route
login_manager.login_message_category = "info"  # replicate flash msg but for login
# configuration for sending mails
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
# to avoid circular import problem
from flaskblog import routes
