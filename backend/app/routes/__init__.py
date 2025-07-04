from flask import Blueprint
from .auth import auth_bp
from .users import users_bp
from .video import video_bp
from .heatmap import heatmap_bp
from .pdf_generator import pdf_generator_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(heatmap_bp)
    app.register_blueprint(pdf_generator_bp)


