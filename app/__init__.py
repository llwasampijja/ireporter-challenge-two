from flask import Flask
from flask_jwt_extended import JWTManager
import os
from app.views.redflag_view import redflag_bp


def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom(12)
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)
    app.register_blueprint(redflag_bp, url_prefix="/api/v1/red-flags")
    return app