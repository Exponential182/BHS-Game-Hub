from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    BooleanField,
    EmailField,
    FileField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, EqualTo, Length

from helpers import AllowedWebZip, FileSizeLimit


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
            Length(min=1, max=100),
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
            "Complete", "Beta", "Prototype"
        ],
    )
    cover_image = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "JPEG's and PNG's only!"),
            FileSizeLimit(5)
        ],
        render_kw={"accept": ".jpg,.jpeg,.png"},
    )
    web_game_upload = FileField(
        validators=[
            FileAllowed(["zip"], "ZIP archives only"),
            FileSizeLimit(512),
            AllowedWebZip(512),
        ],
        render_kw={"accept": ".zip"},
    )
    downloadable_game_upload = FileField(
        validators=[
            FileAllowed(
                ["exe", "zip", "gz", "tar.gz", "app", "dmg"],
                "Invalid file type (try exe, zip, or .tar.gz)"
            ),
            FileSizeLimit(1024)
        ],
        render_kw={"accept": ".exe,.zip,.gx,tar.gz,.app,.dmg"}
    )
    has_windows = BooleanField(label="Windows")
    has_mac = BooleanField("Mac")
    has_linux = BooleanField("Linux")
    save = SubmitField("Save")
