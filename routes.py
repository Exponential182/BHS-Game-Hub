from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import select
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.exc import NoResultFound

from models import Game, Jam, User
from forms import LoginForm, SignupForm
from extensions import hasher, db, login_manager

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    statement = select(User).limit(1).where(User.id == int(user_id))
    data = db.session.execute(statement)
    data = data.scalar()
    if data is None:
        return None
    return data


@main_bp.route("/")
def home():
    return render_template("home.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
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
            pass  # Error Message for failing (TO BE IMPLEMENTED)
    return render_template("login.html", form=login_form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
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
            # send error message about invalid password
            pass
    return render_template("signup.html", form=signup_form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@main_bp.route("/games")
def games():
    return render_template("games.html")
