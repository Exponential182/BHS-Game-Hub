from argon2.exceptions import VerifyMismatchError
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from extensions import db, hasher, login_manager
from forms import LoginForm, SignupForm
from models import Game, Genre, Jam, User

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)


# Flask-login's internal user loader (deprecated for lookups by current_user)
@login_manager.user_loader
def load_user(user_id):
    """Loads a users data by id, returns a User Object"""
    statement = select(User).limit(1).where(User.id == int(user_id))
    data = db.session.execute(statement)
    data = data.scalar()
    if data is None:
        return None
    return data


@main_bp.route("/")
def home():
    """Render the home page."""
    return render_template("home.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Render the login page and validate login credentials."""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        try:
            statement = select(User).where(User.username == username)
            user_info = db.session.execute(statement.limit(1)).one()
            user_info: User = user_info[0]
        except NoResultFound:
            return redirect(url_for("auth.signup"))
        try:
            if hasher.verify(user_info.password_hash, password):
                login_user(user_info, remember=login_form.remember.data)
                return redirect(url_for("main.home"))
        except VerifyMismatchError:
            flash("Incorrect Username or Password")
    return render_template("login.html", form=login_form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """Render the signup page and add new users to database."""
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data
        repeat_password = signup_form.repeat_password.data
        if password == repeat_password:
            statement = select(User).where(User.email == email)
            user_info = db.session.execute(statement.limit(1)).first()
            if user_info:
                return redirect(url_for("auth.login"))  # Add error message?

            new_user = User(
                email=email,
                username=username,
                password_hash=hasher.hash(password),
                is_admin=False,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            flash("The passwords didn't match.")
    return render_template("signup.html", form=signup_form)


@auth_bp.route("/logout")
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("main.home"))


@main_bp.route("/games")
def games():
    """Render the game catelouge page."""
    statement = select(Game)
    genre_search = request.args.get("genre", default=None)

    if genre_search is not None:
        statement = statement.join(Genre).where(Genre.name == genre_search)

    genres = db.session.execute(select(Genre)).scalars()
    game_info = db.session.execute(statement).scalars().all()
    return render_template(
        "games.html",
        game_data=game_info,
        genre_data=genres,
    )


@main_bp.route("/game/<int:game_id>")
def game_page(game_id):
    """Render the game specific page"""
    game_stmt = select(Game).where(Game.id == game_id)

    game_info = db.session.execute(game_stmt).scalar_one_or_none()
    if game_info is None:
        abort(404)
    return render_template("game.html", game_data=game_info)


@main_bp.route("/download/<path:file_path>")
def download(file_path):
    return send_from_directory(
        current_app.config["DOWNLOAD_FOLDER"],
        file_path,
        as_attachment=True,
    )


# Redirect errors to specific pages to better handle crashes/bad urls.
@main_bp.app_errorhandler(404)
def page_not_found(_error):
    """Render the 404 error page."""
    _error = _error  # Fixes unsued variable errors.  # noqa: PLW0127

    # Removes layout from errors in iframes.
    if request.endpoint == "static":
        return render_template("static_404.html")

    return render_template("404.html")


@main_bp.app_errorhandler(500)
def internal_server_error(_error):
    """Render the 500 error page."""
    _error = _error  # Fixes unsued variable errors.  # noqa: PLW0127

    # Removes layout from errors in iframes.
    if request.endpoint == "static":
        return render_template("static_500.html")

    return render_template("500.html")
