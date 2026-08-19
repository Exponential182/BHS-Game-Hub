from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    FileField,
    MultipleFileField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    """Form template for login page."""

    username = StringField(
        "Username",
        render_kw={"placeholder": "Username"},
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=32,
                message="Usernames must be between 4 and 32 characters",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Password"},
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=64,
                message="Passwords must be between 8 and 64 characters.",
            ),
        ],
    )
    remember = BooleanField("Remember Me?")
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    """Form template for signup page."""

    email = EmailField(
        "Email",
        render_kw={"placeholder": "Email"},
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=320,
                message="Invalid Email Address"
            ),
        ],
    )
    username = StringField(
        "Username",
        render_kw={"placeholder": "Username"},
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=32,
                message="Usernames must be between 4 and 32 characters",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Password"},
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=64,
                message="Passwords must be between 8 and 64 characters.",
            ),
        ],
    )
    repeat_password = PasswordField(
        "Repeat Password",
        render_kw={"placeholder": "Confirm Password"},
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=64,
                message="Passwords must be between 8 and 64 characters.",
            ),
            EqualTo(
                "password",
                message="Passwords do not match."
            )
        ],
    )
    remember = BooleanField("Remember Me?")
    submit = SubmitField("Submit")


class GameEditForm(FlaskForm):
    """Game Upload and Configuration Form"""
    # Name, tagline, description, genre, visibility, dev_state, cover_image, images
    # Maybes: tags, genre multiselect

    name = StringField(
        label="Title",
        validators=[
            DataRequired(
                message="This field is requried"
            ),
            Length(
                min=1,
                max=100,
                message="Game titles must be between 1 and 100 characters",
            ),
        ],
    )
    tagline = StringField(
        description="A brief summary of your game for use on the home page.",
        validators=[
            Length(min=1, max=50),
        ]
    )

    # Phantom field, hidden in page, to fill data into with js from quill
    description = StringField()
    genre = SelectField(
        choices=["No Genres Available"]
    )
    visibility = RadioField(
        DataRequired(),
        coerce=int,
        choices=[
            (1, "Visible ‒‒ Anyone can view the game"),
            (0, "Private ‒‒ Only you can view the game"),
        ],
    )
    dev_state = RadioField(
        DataRequired(),
        choices=[
            "Complete", "Beta", "Prototype"],
    )
    cover_image = FileField()
    images = MultipleFileField()
    game_uploads = MultipleFileField()
    save = SubmitField("Save")
