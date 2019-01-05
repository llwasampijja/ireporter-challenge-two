from flask import Flask, Response, json
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os

from app.views.redflag_view import redflag_bp
from app.views.users_view import user_bp
from app.views.auth_view import auth_bp
from app.views.intervention_view import intervention_bp
from app.views.error_handlers_view import page_not_found, method_not_allowed, bad_request_error
from app.utilitiez.static_strings import SWAGGER_UI_URL, API_URL, URL_LOGIN, URL_REGISTER, URL_INTERVENTIONS, URL_REDFLAGS, URL_USERS


def create_app():
    


    app = Flask(__name__)

    app.secret_key = os.urandom(12)
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)

    app.register_blueprint(redflag_bp, url_prefix="/api/v1/red-flags")
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(intervention_bp, url_prefix="/api/v1/interventions")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(400, bad_request_error)

    swagger_ui_bp = get_swaggerui_blueprint(SWAGGER_UI_URL, API_URL)
    app.register_blueprint(swagger_ui_bp, url_prefix=SWAGGER_UI_URL)
    
    return app