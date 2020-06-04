from flask_wtf import FlaskForm
from wtforms import StringField  #
from wtforms import SubmitField  # submit form
from wtforms import TextAreaField  # for post content
from wtforms.validators import DataRequired  # make data entry mandatory for field


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
