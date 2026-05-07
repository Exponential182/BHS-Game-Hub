from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from argon2 import PasswordHasher


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
hasher = PasswordHasher(time_cost=3, parallelism=4, memory_cost=65536)
