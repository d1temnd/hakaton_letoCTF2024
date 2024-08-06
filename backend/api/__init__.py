from flask import Blueprint
from .auth import auth_bp
from .scoreboard import scoreboard_bp
from .get_task import get_task_bp
from .profile import profile_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(scoreboard_bp)
    app.register_blueprint(get_task_bp)
    app.register_blueprint(profile_bp)