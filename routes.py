from flask import render_template
from models import Game, Jam, User
from forms import LoginForm


def init_routes(app, login_manager):
    @app.route("/")
    def home():
        return render_template("home.html")
