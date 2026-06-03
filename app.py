from flask import Flask
from extensions import db, login_manager
from routes import main_bp, auth_bp
from context_processors import utilities


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = """
        ab4cdb98da867b286998c0fcabe0e4cfd58486d007fe9c2b2ce5c39f398713ec
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game_hub.db"

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.context_processor(utilities)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
