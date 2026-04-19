from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField, PasswordField,
                     BooleanField, EmailField)
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=50),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=100),
        ],
    )
    remember = BooleanField("Remember Me?")
    sumbit = SubmitField("Submit")


class SignupForm(FlaskForm):
    email = EmailField(
        "Email (Must be a burnside.school.nz)",
        validators=[
            DataRequired()
        ],
    )
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=50)
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=100)
        ],
    )
    repeat_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            Length(min=8, max=100),
            EqualTo(password),
        ],
    )
    remember = BooleanField("Remember Me?")
    sumbit = SubmitField("Submit")
