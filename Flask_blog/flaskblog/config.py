import os


class Config:
    # secret key for protection against modifying cookies, forgery attaacks etc.
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"  # sqlite db path
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # suppresses deprecation warning

    # configuration for sending mails
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
