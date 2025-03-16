from flask import Blueprint
from .auth import auth_bp
from .users import users_bp
from .video import video_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp)
    app.register_blueprint(video_bp)


