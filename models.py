from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import Base


class Game(Base):
    """A Registered Game in the database.
    Links to associated Users and Jams.
    """

    __tablename__ = "Game"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    tagline: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    html_game_path: Mapped[str] = mapped_column()
    has_html: Mapped[bool] = mapped_column()
    download_game_path: Mapped[str] = mapped_column()
    has_windows: Mapped[bool] = mapped_column()
    has_mac: Mapped[bool] = mapped_column()
    has_linux: Mapped[bool] = mapped_column()
    cover_image_url: Mapped[str] = mapped_column()
    visibility: Mapped[bool] = mapped_column()
    dev_state: Mapped[str] = mapped_column()
    last_updated: Mapped[int] = mapped_column()

    # One to Many Links
    genre_id: Mapped[int] = mapped_column(ForeignKey("Genre.id"))
    genre: Mapped["Genre"] = relationship(back_populates="games")

    # Many to Many Link
    users: Mapped[list["User"]] = relationship(
        secondary="UserGame",
        back_populates="games",
    )


class User(Base, UserMixin):
    """A Registered User in the database.
    Links to associated Games
    """

    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    is_admin: Mapped[bool] = mapped_column()

    # Many to Many Links
    games: Mapped[list["Game"]] = relationship(
        secondary="UserGame",
        back_populates="users",
    )


class Genre(Base):
    """Describes the genre of a game."""

    __tablename__ = "Genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    games: Mapped[list["Game"]] = relationship(back_populates="genre")


class UserGame(Base):
    """Association table for Users and Games."""

    __tablename__ = "UserGame"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
        primary_key=True,
    )
    game_id: Mapped[int] = mapped_column(
        ForeignKey("Game.id"),
        primary_key=True,
    )
