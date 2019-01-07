"""this module servers the purpose of declaring app as a package
and also as an application factory"""
import os

from flask import Flask, Response, json
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from app.views.redflag_view import redflag_blueprint
from app.views.users_view import user_blueprint
from app.views.auth_view import auth_blueprint
from app.views.intervention_view import intervention_blueprint
from app.views.error_handlers_view import (
    page_not_found,
    method_not_allowed,
    bad_request_error
)
from app.utilitiez.static_strings import (
    SWAGGER_UI_URL,
    API_URL,
    URL_LOGIN,
    URL_REGISTER,
    URL_INTERVENTIONS,
    URL_REDFLAGS,
    URL_USERS
)

def create_app():
    """this is the application factory function, configuration, registering, etc happen here"""
    app = Flask(__name__)

    app.secret_key = os.urandom(12)
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)

    app.register_blueprint(redflag_blueprint, url_prefix="/api/v1/red-flags")
    app.register_blueprint(user_blueprint, url_prefix="/api/v1/users")
    app.register_blueprint(intervention_blueprint, url_prefix="/api/v1/interventions")
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(400, bad_request_error)

    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_UI_URL, API_URL)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_UI_URL)

    return app
