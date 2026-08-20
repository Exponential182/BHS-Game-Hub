from flask import Flask

# Pulls in all of the required functions/objects
from context_processors import utilities
from extensions import db, login_manager
from routes import auth_bp, main_bp


def create_app():
    """Instance the app and establishes all conenctions."""
    app = Flask(__name__)

    # Insecure key, to be replaced before deployment.
    app.config["SECRET_KEY"] = """
        ab4cdb98da867b286998c0fcabe0e4cfd58486d007fe9c2b2ce5c39f398713ec
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game_hub.db"
    # Requires additional Filtering
    app.config["DOWNLOAD_FOLDER"] = "static/games/"
    app.config["UPLOAD_FOLDER"] = "static/games/"

    # 1.56 GB to account for game uploads
    app.config["MAX_CONTENT_LENGTH"] = 1600 * 1024 * 1024

    # Instance all imported objects
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
