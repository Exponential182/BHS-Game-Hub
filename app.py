from flask import Flask
from routes import init_routes
from models import Game, User, Jam, Base

# SQL Alchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
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


init_routes(app)
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game_hub.db"
db.init_app(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
