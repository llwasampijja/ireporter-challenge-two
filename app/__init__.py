from flask import Flask
from flask_jwt_extended import JWTManager
import os

from app.views.redflag_view import redflag_bp
from app.views.users_view import user_bp


def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom(12)
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)

    app.register_blueprint(redflag_bp, url_prefix="/api/v1/red-flags")
    app.register_blueprint(user_bp, url_prefix="/api/v1/auth/users")
    return app