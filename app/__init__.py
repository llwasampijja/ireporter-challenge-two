from flask import Flask
from app.views.redflag_view import redflag_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(redflag_bp, url_prefix="/api/v1/red-flags")
    return app