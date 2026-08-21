from pathlib import Path
from shutil import rmtree
from time import time
from zipfile import ZipFile

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
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from extensions import cleaner, db, hasher, login_manager
from forms import GameEditForm, LoginForm, SignupForm
from helpers import crop_and_centre_cover_image
from models import Game, GameFile, Genre, User

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)

base_directory = Path(__file__).resolve().parent


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
            flash("Incorrect Username or Password. <br> The account may not exist.")
            return redirect(url_for("auth.login"))
        try:
            if hasher.verify(user_info.password_hash, password):
                login_user(user_info, remember=login_form.remember.data)
                return redirect(url_for("main.games"))
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
                flash("An account already exists with that email.")
                return redirect(url_for("auth.login"))

            new_user = User(
                email=email,
                username=username,
                password_hash=hasher.hash(password),
                is_admin=False,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=signup_form.remember)
            return redirect(url_for("main.games"))
        else:
            flash("The passwords didn't match.")
    return render_template("signup.html", form=signup_form)


@auth_bp.route("/logout")
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("main.home"))


@main_bp.route("/")
def games():
    """Render the game catelouge page."""
    statement = select(Game).order_by(Game.last_updated.desc())
    statement = statement.where(Game.visibility)
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


@main_bp.route("/game/edit/<int(signed=True):game_id>", methods=["GET", "POST"])
@login_required
def edit_game(game_id):
    game_edit_form = GameEditForm()

    game_valid_stmt = select(Game).where(Game.id == game_id)
    game_data = db.session.execute(game_valid_stmt).one_or_none()
    if game_data is None:
        flash("Game does not exist!")
        return redirect(url_for("main.games"))
    game_data: Game = game_data[0]

    # Populate Genres for display and validation
    genres = list(db.session.execute(select(Genre.name)).all())
    genres = [row[0] for row in genres]  # Fix Format
    game_edit_form.genre.choices = genres

    if request.method == "POST":
        if game_edit_form.validate_on_submit():
            # Shortening for writeability
            form = game_edit_form

            cleaned_html = cleaner.clean(game_edit_form.description.data)
            game_data.description = cleaned_html

            image_file = form.cover_image.data
            if image_file:
                image_file = FileStorage(
                    crop_and_centre_cover_image(image_file)
                )
                cover_image_path = f"static/games/{game_id}/cover_image.png"
                save_path = Path(base_directory / cover_image_path)
                save_path.parent.mkdir(parents=True, exist_ok=True)
                image_file.save(save_path)
                game_data.cover_image_url = cover_image_path
            else:
                game_data.cover_image_url = "/static/images/default_cover_image.png"

            web_upload = form.web_game_upload.data
            if web_upload:
                web_upload.stream.seek(0)
                zipped_web = ZipFile(web_upload.stream, "r")

                initial_extract_path = Path(
                    base_directory / f"static/games/{game_id}/game_files/web_new/"
                )
                backup_path = Path(
                    base_directory / f"static/games/{game_id}/game_files/web_old/"
                )
                primary_path = Path(
                    base_directory / f"static/games/{game_id}/game_files/web/"
                )

                if not primary_path.is_dir():
                    primary_path.mkdir(parents=True, exist_ok=True)

                primary_path.rename(backup_path)

                if initial_extract_path.is_dir():
                    rmtree(initial_extract_path)

                initial_extract_path.mkdir(parents=True, exist_ok=True)
                try:
                    zipped_web.extractall(initial_extract_path)
                    extract_success = True
                except ValueError:
                    backup_path.rename(primary_path)
                    extract_success = False

                if extract_success:
                    initial_extract_path.rename(primary_path)
                    rmtree(backup_path)

                    old_web_game = db.session.execute(
                        select(GameFile).where(
                            GameFile.game_id == game_id
                        ).where(GameFile.is_html5)
                    ).one_or_none()
                    if old_web_game:
                        db.session.remove(old_web_game[0])

                    file_info = GameFile(
                        game_id=game_id,
                        path=(
                            str(primary_path.relative_to(base_directory)) + "/index.html"
                        ),
                        is_html5=True,
                        is_windows=False,
                        is_mac=False,
                        is_linux=False,
                    )
                    db.session.add(file_info)
                    db.session.commit()

            downloadable_game = form.downloadable_game_upload.data
            if downloadable_game:
                game: FileStorage = downloadable_game
                old_game_stmt = select(GameFile).where(
                    GameFile.game_id == game_id
                ).where(
                    GameFile.is_html5 == False
                )

                old_game = db.session.execute(old_game_stmt).one_or_none()
                print(old_game)
                if old_game:
                    old_game: GameFile = old_game[0]
                    old_game_path: Path = Path(
                        base_directory / old_game.path.lstrip("/")
                    )

                    if old_game_path.is_file():
                        old_game_path.unlink()
                    db.session.delete(old_game)
                    db.session.commit()

                target_folder = f"static/games/{game_id}/game_files"
                target_folder = Path(base_directory / target_folder)
                target_folder.mkdir(parents=True, exist_ok=True)
                file_name = secure_filename(game.filename)
                target_file = Path(target_folder / file_name)
                game.save(target_file)

                print(str((target_file.relative_to(base_directory)).resolve()))
                new_game = GameFile(
                    game_id=game_id,
                    path=str(target_file.relative_to(base_directory).resolve()),
                    is_html5=False,
                    is_windows=form.has_windows.data,
                    is_mac=form.has_mac.data,
                    is_linux=form.has_linux.data,
                )
                db.session.add(new_game)
                db.session.commit()

            game_data.name = form.name.data
            game_data.visibility = form.visibility.data
            game_data.last_updated = int(time())
            game_data.users.append(current_user)

            db.session.commit()
            flash("Game Saved successfully")
            return redirect(url_for("main.games"))
        else:
            flash("Bad input")
            return render_template("game_form.html", form=game_edit_form)

    # Prefill form
    game_edit_form.name.data = game_data.name
    game_edit_form.tagline.data = game_data.tagline
    game_edit_form.description.data = game_data.description
    if game_data.genre:
        game_edit_form.genre.data = game_data.genre.name
    if game_data.cover_image_url:
        game_edit_form.cover_image.description = game_data.cover_image_url
    game_edit_form.visibility.data = game_data.visibility
    game_edit_form.dev_state.data = game_data.dev_state

    return render_template("game_form.html", form=game_edit_form)


@main_bp.route("/newgame")
def new_game():
    new_game_data = Game(visibility=0)
    db.session.add(new_game_data)
    db.session.commit()
    new_game_id = new_game_data.id
    return redirect(url_for('main.edit_game', game_id=new_game_id))


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
