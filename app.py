from flask import Flask, render_template, redirect, flash
from datetime import datetime

# SQL Alchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship)
from sqlalchemy import String, Integer, ForeignKey, select
from sqlalchemy.exc import NoResultFound

# Forms
from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField, PasswordField,
                     BooleanField)
from wtforms.validators import DataRequired, Length, NumberRange

# Passwords
from flask_login import (LoginManager, UserMixin, current_user, login_user,
                         login_required, logout_user)
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


app = Flask(__name__)
app.config["SECRET_KEY"] = """
    ab4cdb98da867b286998c0fcabe0e4cfd58486d007fe9c2b2ce5c39f398713ec
"""
login_manager = LoginManager()
hasher = PasswordHasher(time_cost=3, parallelism=4, memory_cost=65536)


# Tables
class Base(DeclarativeBase):
    pass


class Game(Base):
    __tablename__ = "Game"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()
    is_html5: Mapped[bool] = mapped_column()
    is_downloadable: Mapped[bool] = mapped_column()
    genre: Mapped[str] = mapped_column()
    tags: Mapped[str] = mapped_column()
    image_url: Mapped[str] = mapped_column()
    overall_rating: Mapped[float] = mapped_column()
    rating_count: Mapped[int] = mapped_column()
    users: Mapped[list["User"]] = relationship(
        secondary="UserGame",
        back_populaes="games",
    )
    jams: Mapped[list["Jam"]] = relationship(
        secondary="JamGame",
        back_populates="games",
    )


class User(Base, UserMixin):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    is_admin: Mapped[bool] = mapped_column()
    games: Mapped[list["Game"]] = relationship(
        secondary="UserGame",
        back_populates="users",
    )
    jams: Mapped[list["Jam"]] = relationship(
        secondary="UserJam",
        back_populates="users"
    )


class Jam(Base):
    __tablename__ = "Jam"
    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    start_time: Mapped[datetime] = mapped_column(String)
    end_time: Mapped[datetime] = mapped_column(String)
    users: Mapped[list["User"]] = relationship(
        secondary="UserJam",
        back_populates="jams",
    )
    games: Mapped[list["Game"]] = relationship(
        secondary="JamGame",
        back_populates="jams",
    )


class UserJam(Base):
    __tablename__ = "UserJam"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
        primary_key=True,
    )
    jam_id: Mapped[int] = mapped_column(
        ForeignKey("Jam.id"),
        primary_key=True,
    )


class UserGame(Base):
    __tablename__ = "UserGame"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
        primary_key=True,
    )
    game_id: Mapped[int] = mapped_column(
        ForeignKey("Game.id"),
        primary_key=True,
    )


class JamGame(Base):
    __tablename__ = "JamGame"
    game_id: Mapped[int] = mapped_column(
        ForeignKey("Game.id"),
        primary_key=True,
    )
    jam_id: Mapped[int] = mapped_column(
        ForeignKey("Jam.id"),
        primary_key=True,
    )


db = SQLAlchemy(model_class=Base)


# Forms
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
            DataRequired(), Length(min=4, max=50)
        ]
    )
    password = PasswordField("Password", validators=[
            DataRequired(), Length(min=8, max=100)
        ]
    )
    remember = BooleanField("Remember Me?")
    sumbit = SubmitField("Submit")


@login_manager.user_loader
def load_user(user_id):
    statement = select(User).limit(1).where(User.id == int(user_id))
    data = db.session.execute(statement)
    data = data.scalar()
    if data is None:
        return None
    return User(id=data.id)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game_hub.db"
db.init_app(app)
login_manager.init_app(app)


@app.route("/")
def home():
    return "10"


if __name__ == "__main__":
    app.run(debug=True)
