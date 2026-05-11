from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from flask_login import UserMixin

from extensions import Base


class Game(Base):
    __tablename__ = "Game"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    has_html5: Mapped[bool] = mapped_column()
    html5_file_path: Mapped[str] = mapped_column()
    has_windows: Mapped[bool] = mapped_column()
    windows_file_path: Mapped[str] = mapped_column()
    has_mac: Mapped[bool] = mapped_column()
    mac_file_path: Mapped[str] = mapped_column()
    has_linux: Mapped[bool] = mapped_column()
    linux_file_path: Mapped[str] = mapped_column()
    genre: Mapped[str] = mapped_column()
    tags: Mapped[str] = mapped_column()
    image_url: Mapped[str] = mapped_column()
    overall_rating: Mapped[float] = mapped_column()
    rating_count: Mapped[int] = mapped_column()
    users: Mapped[list["User"]] = relationship(
        secondary="UserGame",
        back_populates="games",
    )
    jams: Mapped[list["Jam"]] = relationship(
        secondary="JamGame",
        back_populates="games",
    )


class User(Base, UserMixin):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
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
    id: Mapped[int] = mapped_column(primary_key=True)
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
