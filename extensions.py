from argon2 import PasswordHasher
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Not created in models.py so database can be delceared with hasher,
# login manager, etc.
class Base(DeclarativeBase):
    """Base Class for all databse tables."""


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
hasher = PasswordHasher(time_cost=3, parallelism=4, memory_cost=65536)
