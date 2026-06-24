from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from flask_login import UserMixin

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
    has_html: Mapped[bool] = mapped_column()
    html_file_path: Mapped[str] = mapped_column()
    has_windows: Mapped[bool] = mapped_column()
    windows_file_path: Mapped[str] = mapped_column()
    has_mac: Mapped[bool] = mapped_column()
    mac_file_path: Mapped[str] = mapped_column()
    has_linux: Mapped[bool] = mapped_column()
    linux_file_path: Mapped[str] = mapped_column()
    tags: Mapped[str] = mapped_column()
    image_url: Mapped[str] = mapped_column()
    overall_rating: Mapped[float] = mapped_column()
    rating_count: Mapped[int] = mapped_column()

    # One to Many Links
    genre_id: Mapped[int] = mapped_column(ForeignKey("Genre.id"))
    genre: Mapped["Genre"] = relationship(back_populates="games")

    # Many to Many Link
    users: Mapped[list["User"]] = relationship(
        secondary="UserGame",
        back_populates="games",
    )
    jams: Mapped[list["Jam"]] = relationship(
        secondary="JamGame",
        back_populates="games",
    )


class User(Base, UserMixin):
    """A Registered User in the database.
    Links to associated Games and Jams
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
    jams: Mapped[list["Jam"]] = relationship(
        secondary="UserJam",
        back_populates="users"
    )


class Jam(Base):
    """A Registered Jam in the database.
    Links to associated Users and Games
    """
    __tablename__ = "Jam"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    start_time: Mapped[datetime] = mapped_column(String)
    end_time: Mapped[datetime] = mapped_column(String)

    # Many to Many Links
    users: Mapped[list["User"]] = relationship(
        secondary="UserJam",
        back_populates="jams",
    )
    games: Mapped[list["Game"]] = relationship(
        secondary="JamGame",
        back_populates="jams",
    )


class Genre(Base):
    """Describes the genre of a game."""
    __tablename__ = "Genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    games: Mapped[list["Game"]] = relationship(back_populates="genre")


# Linking tables
class UserJam(Base):
    """Association table for Users and Jams."""
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


class JamGame(Base):
    """Association table for Games and Jams."""
    __tablename__ = "JamGame"
    game_id: Mapped[int] = mapped_column(
        ForeignKey("Game.id"),
        primary_key=True,
    )
    jam_id: Mapped[int] = mapped_column(
        ForeignKey("Jam.id"),
        primary_key=True,
    )
