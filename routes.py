from flask import Flask, render_template, redirect
from models import Game, Jam, User
from forms import LoginForm, SignupForm

from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, current_user, login_user,
                         login_required, logout_user)
from sqlalchemy import select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from sqlalchemy.exc import NoResultFound

hasher = PasswordHasher(time_cost=3, parallelism=4, memory_cost=65536)


def init_routes(app: Flask, login_manager: LoginManager, db: SQLAlchemy):
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/login", methods=["GET", "POST"])
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
                return redirect("/signup")
            try:
                if hasher.verify(user_info.password_hash, password):
                    login_user(user_info, login_form.remember.data)
                    return redirect("/")
            except VerifyMismatchError:
                pass  # Error Message for failing (TO BE IMPLEMENTED)
        return render_template("login.html", form=login_form)

    @app.route("/signup", methods=["GET", "POST"])
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
                    return redirect("/login")  # Add error message?

                new_user = User(
                    email=email,
                    username=username,
                    password_hash=hasher.hash(password),
                    is_admin=False,
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect("/login")
            else:
                # send error message about invalid password
                pass
        return render_template("signup.html", form=signup_form)
