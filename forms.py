from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField,
                     BooleanField, EmailField)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Form template for login page."""
    username = StringField(
        "Username",
        render_kw={
            "placeholder": "Username"
        },
        validators=[
            DataRequired(),
            Length(min=4, max=32),
        ],
    )
    password = PasswordField(
        "Password",
        render_kw={
            "placeholder": "Password"
        },
        validators=[
            DataRequired(),
            Length(min=8, max=64),
        ],
    )
    remember = BooleanField("Remember Me?")
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    """Form template for signup page."""
    email = EmailField(
        "Email",
        render_kw={
            "placeholder": "Email"
        },
        validators=[
            DataRequired(),
            Length(min=1, max=320),
        ],
    )
    username = StringField(
        "Username",
        render_kw={
            "placeholder": "Username"
        },
        validators=[
            DataRequired(),
            Length(min=4, max=32)
        ],
    )
    password = PasswordField(
        "Password",
        render_kw={
            "placeholder": "Password"
        },
        validators=[
            DataRequired(),
            Length(min=8, max=64)
        ],
    )
    repeat_password = PasswordField(
        "Repeat Password",
        render_kw={
            "placeholder": "Confirm Password"
        },
        validators=[
            DataRequired(),
            Length(min=8, max=64),
        ],
    )
    submit = SubmitField("Submit")
