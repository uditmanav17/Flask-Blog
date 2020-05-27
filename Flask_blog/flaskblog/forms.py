from flask_wtf import FlaskForm
from flask_wtf.file import FileField  # for user image upload
from flask_wtf.file import FileAllowed  # check uploaded file img ext
from flask_login import current_user  # access current user info
from wtforms import StringField  #
from wtforms import PasswordField  # hide password while entering
from wtforms import SubmitField  # submit form
from wtforms import BooleanField
from wtforms import TextAreaField  # for post content
from wtforms.validators import DataRequired  # make data entry mandatory for field
from wtforms.validators import Length  # constraint on field
from wtforms.validators import Email  # check mail authentication
from wtforms.validators import EqualTo  # for confirm password field
from wtforms.validators import ValidationError  # Raise error if condition not met
from flaskblog.models import User  # import user model to validate user names

# create registration form class
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match!"),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Check if a user exists with username specified in registraion form"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken, please choose another.")

    def validate_email(self, email):
        """Check if a email exists with email specified in registraion form"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already taken, please choose another.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already taken, please choose another.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already taken, please choose another.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email. You must register first."
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")

