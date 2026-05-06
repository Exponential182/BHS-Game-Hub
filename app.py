from flask import Flask
from routes import init_routes
from models import User, Base

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


app = Flask(__name__)
app.config["SECRET_KEY"] = """
    ab4cdb98da867b286998c0fcabe0e4cfd58486d007fe9c2b2ce5c39f398713ec
"""
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    statement = select(User).limit(1).where(User.id == int(user_id))
    data = db.session.execute(statement)
    data = data.scalar()
    if data is None:
        return None
    return data


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game_hub.db"
db.init_app(app)
login_manager.init_app(app)
init_routes(app, login_manager, db)

if __name__ == "__main__":
    app.run(debug=True)
