from flask import Blueprint
from .auth import auth_bp
from .scoreboard import scoreboard_bp
from .get_task import get_task_bp
from .profile import profile_bp
from .admin_start_game import admin_start_game_bp
from .pass_task import pass_task_bp
from .user import user_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(scoreboard_bp)
    app.register_blueprint(get_task_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_start_game_bp)
    app.register_blueprint(pass_task_bp)
    app.register_blueprint(user_bp)
