from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os

from app.views.redflag_view import redflag_bp
from app.views.users_view import user_bp
from app.views.intervention_view import intervention_bp


def create_app():
    SWAGGER_UI_URL = "/api/v1/docs"
    API_URL = "https://llwasampijja.github.io/ireporter-challenge-two/swagger.json" #remote API documenation url
    # APi_URL = "http://localhost/swagger-ui/dist/ireporter_challenge_two.json" #local API documentation url


    app = Flask(__name__)

    app.secret_key = os.urandom(12)
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)

    swagger_ui_bp = get_swaggerui_blueprint(SWAGGER_UI_URL, API_URL)
    app.register_blueprint(swagger_ui_bp, url_prefix=SWAGGER_UI_URL)

    app.register_blueprint(redflag_bp, url_prefix="/api/v1/red-flags")
    app.register_blueprint(user_bp, url_prefix="/api/v1/auth/users")
    app.register_blueprint(intervention_bp, url_prefix="/api/v1/interventions")
    return app