from argon2 import PasswordHasher
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from nh3 import Cleaner
from sqlalchemy.orm import DeclarativeBase

from config import ALLOWED_ATTRIBUTES, ALLOWED_TAGS, URL_HEADERS


# Not created in models.py so database can be delceared with hasher,
# login manager, etc.
class Base(DeclarativeBase):
    """Base Class for all databse tables."""


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
hasher = PasswordHasher(time_cost=3, parallelism=4, memory_cost=65536)
cleaner = Cleaner(
    tags=ALLOWED_TAGS,
    attributes=ALLOWED_ATTRIBUTES,
    url_schemes=URL_HEADERS
)
